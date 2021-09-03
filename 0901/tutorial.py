import os
import shutil
import tempfile
import matplotlib.pyplot as plt
import PIL
import torch
import numpy as np
from sklearn.metrics import classification_report

import monai
import matplotlib
from monai.apps import download_and_extract
from monai.config import print_config
from monai.data import decollate_batch
from monai.metrics import ROCAUCMetric
from monai.networks.nets import DenseNet121
from monai.transforms import (
    Activations,
    AddChannel,
    AsDiscrete,
    Compose,
    LoadImage,
    RandFlip,
    RandRotate,
    RandZoom,
    ScaleIntensity,
    EnsureType,
)
from monai.utils import set_determinism


# print_config()
def tutorial():
    # os.environ => 환경 변수 읽어오기
    directory = os.environ.get("MONAI_DATA_DIRECTORY")
    # mkdtemp() = > 임시 디렉토리 생성  (directory가 None일 경우)
    # root_dir = tempfile.mkdtemp() if directory is None else directory
    root_dir = os.path.join(".\\")
    print(root_dir)

    resource = "https://drive.google.com/uc?id=1QsnnkvZyJPcbRoV_ArW8SnE1OTuoVbKE"
    md5 = "0bc7306e7427e00ad1c5526a6677552d"

    compressed_file = os.path.join(root_dir, "MedNIST.tar.gz")
    data_dir = os.path.join(root_dir, "MedNIST")
    # if not os.path.exists(data_dir):
    #     download_and_extract(resource, compressed_file, root_dir, md5)
        # download_and_extract(url, filepath, output_dir, hash_type)
        # => URL에서 파일을 다운로드하고 출력 디렉토리에 압축 품

    # 모듈의 랜덤 시드를 설정하여 deterministic training을 활성화하거나 비활성화
    set_determinism(seed=0)

    # data_dir에서 directory만 추출
    class_names = sorted(x for x in os.listdir(data_dir)
                         if os.path.isdir(os.path.join(data_dir, x)))
    print("class_names = ",class_names)
    num_class = len(class_names)
    # 하위 경로의 이미지들 리스트에 저장
    image_files = [
        [
            os.path.join(data_dir, class_names[i], x)
            for x in os.listdir(os.path.join(data_dir, class_names[i]))
        ]
        for i in range(num_class)
    ]

    # 원소별로(폴더별) 사진 개수 카운트
    num_each = [len(image_files[i]) for i in range(num_class)]

    image_files_list = []
    image_class = []
    for i in range(num_class):
        image_files_list.extend(image_files[i]) # 전체 사진을 1차원으로
        image_class.extend([i] * num_each[i])   # 폴더별로 id 지정 0~5

    # 전체 image 개수
    num_total = len(image_class)
    # image 크기(차원or치수) 64x64
    image_width, image_height = PIL.Image.open(image_files_list[0]).size

    print(f"Total image count: {num_total}")
    print(f"Image dimensions: {image_width} x {image_height}")
    print(f"Label names: {class_names}")
    print(f"Label counts: {num_each}")

    # plt.subplots(3, 3, figsize=(8, 8))
    # # 전체 이미지 중 랜덤으로 9개 추출
    # # i => plt 원소 , k => image 원소로 사용
    # for i, k in enumerate(np.random.randint(num_total, size=9)):
    #     im = PIL.Image.open(image_files_list[k])
    #     arr = np.array(im)
    #
    #     # i+1번째 슬롯에 이미지와 class_name 지정
    #     plt.subplot(3, 3, i + 1)
    #     plt.xlabel(class_names[image_class[k]])
    #     plt.imshow(arr, cmap="gray", vmin=0, vmax=255)
    # plt.tight_layout()
    # plt.show()

    # dataset의 10%를 유효성 검사로, 10%를 테스트로 무작위로 선택

    # 58954개 원소 array 생성 후 셔플
    val_frac = 0.1
    test_frac = 0.1
    length = len(image_files_list)
    indices = np.arange(length)
    np.random.shuffle(indices)

    # 1/10  => 5895
    test_split = int(test_frac * length)
    # 11790
    val_split = int(val_frac * length) + test_split
    # 0~5894번째 까지를 testset
    test_indices = indices[:test_split]
    # 5895~11789 까지 유효성 검사
    val_indices = indices[test_split:val_split]
    # 11780~ 끝까지 trainset
    train_indices = indices[val_split:]

    # x => image , y => class_name
    train_x = [image_files_list[i] for i in train_indices]
    train_y = [image_class[i] for i in train_indices]
    val_x = [image_files_list[i] for i in val_indices]
    val_y = [image_class[i] for i in val_indices]
    test_x = [image_files_list[i] for i in test_indices]
    test_y = [image_class[i] for i in test_indices]

    print(
        f"Training count: {len(train_x)}, Validation count: "
        f"{len(val_x)}, Test count: {len(test_x)}")

    train_transforms = Compose(
        [
            LoadImage(image_only=True),
            AddChannel(),
            ScaleIntensity(),
            # 입력 배열 무작위로 회전, prob-회전 확률, keep_size- true일 경우 출렵 모양이 입력과 동일
            RandRotate(range_x=np.pi / 12, prob=0.5, keep_size=True),
            # 랜덤으로 뒤집음
            RandFlip(spatial_axis=0, prob=0.5),
            # 랜덤으로 확대 or 축소
            RandZoom(min_zoom=0.9, max_zoom=1.1, prob=0.5),
            EnsureType(),
        ]
    )

    val_transforms = Compose(
        [LoadImage(image_only=True), AddChannel(), ScaleIntensity(), EnsureType()])

    y_pred_trans = Compose([EnsureType(), Activations(softmax=True)])

    # 원 핫 형식으로 변환, 클래스 개수만큼
    y_trans = Compose([EnsureType(), AsDiscrete(to_onehot=True, n_classes=num_class)])

    class MedNISTDataset(torch.utils.data.Dataset):
        def __init__(self, image_files, labels, transforms):
            self.image_files = image_files
            self.labels = labels
            self.transforms = transforms

        def __len__(self):
            return len(self.image_files)

        def __getitem__(self, index):
            return self.transforms(self.image_files[index]), self.labels[index]

    train_ds = MedNISTDataset(train_x, train_y, train_transforms)
    # 배치당 샘플 수=>300, 모든 epoch에서 데이터 섞기, DataLoad에 사용할 하위 프로세스 수 10
    train_loader = torch.utils.data.DataLoader(
        train_ds, batch_size=300, shuffle=True, num_workers=0) #num_workers 초기에 10이었는데 에러나서 0으로 변경

    val_ds = MedNISTDataset(val_x, val_y, val_transforms)
    val_loader = torch.utils.data.DataLoader(
        val_ds, batch_size=300, num_workers=0)

    test_ds = MedNISTDataset(test_x, test_y, val_transforms)
    test_loader = torch.utils.data.DataLoader(
        test_ds, batch_size=300, num_workers=0)

    # 1. 배치당 모델이 얼마나 업데이트되는지에 대한 학습률을 설정합니다.
    # 2. 셔플 및 임의 변환이 있으므로 총 에포크 번호를 설정하므로 모든 에포크의 훈련 데이터가 다릅니다.
    #    그리고 이것은 시작 튜토리얼일 뿐이므로 4개의 에포크를 훈련시키자.
    #    10 Epoch를 훈련하면 모델은 테스트 데이터 세트에서 100% 정확도를 달성할 수 있습니다.
    # 3. MONAI의 DenseNet을 사용하고 GPU 장치로 이동합니다. 이 DenseNet은 2D 및 3D 분류 작업을 모두 지원할 수 있습니다.
    # 4. Adam 옵티마이저를 사용합니다.

    # 현재 Setup 되어있는 device 확인
    GPU_NUM = 0 # 원하는 GPU 번호 입력
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = DenseNet121(spatial_dims=2, in_channels=1,
                        out_channels=num_class).to(device)
    loss_function = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), 1e-5)
    max_epochs = 4
    val_interval = 1
    auc_metric = ROCAUCMetric()

    # epoch 루프 및 단계 루프를 실행하는 일반적인 PyTorch 교육을 실행하고 모든 epoch 후에 유효성 검사를 수행합니다.
    # 최고의 유효성 검사 정확도를 얻은 경우 모델 가중치를 파일에 저장합니다.

    best_metric = -1
    best_metric_epoch = -1
    epoch_loss_values = []
    metric_values = []

    for epoch in range(max_epochs):
        print("-" * 10)
        print(f"epoch {epoch + 1}/{max_epochs}")
        model.train()
        epoch_loss = 0
        step = 0
        for batch_data in train_loader:
            step += 1
            inputs, labels = batch_data[0].to(device), batch_data[1].to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = loss_function(outputs, labels)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
            print(
                f"{step}/{len(train_ds) // train_loader.batch_size}, "
                f"train_loss: {loss.item():.4f}")
            epoch_len = len(train_ds) // train_loader.batch_size
        epoch_loss /= step
        epoch_loss_values.append(epoch_loss)
        print(f"epoch {epoch + 1} average loss: {epoch_loss:.4f}")

        if (epoch + 1) % val_interval == 0:
            model.eval()
            with torch.no_grad():
                y_pred = torch.tensor([], dtype=torch.float32, device=device)
                y = torch.tensor([], dtype=torch.long, device=device)
                for val_data in val_loader:
                    val_images, val_labels = (
                        val_data[0].to(device),
                        val_data[1].to(device),
                    )
                    y_pred = torch.cat([y_pred, model(val_images)], dim=0)
                    y = torch.cat([y, val_labels], dim=0)
                y_onehot = [y_trans(i) for i in decollate_batch(y)]
                y_pred_act = [y_pred_trans(i) for i in decollate_batch(y_pred)]
                auc_metric(y_pred_act, y_onehot)
                result = auc_metric.aggregate()
                auc_metric.reset()
                del y_pred_act, y_onehot
                metric_values.append(result)
                acc_value = torch.eq(y_pred.argmax(dim=1), y)
                acc_metric = acc_value.sum().item() / len(acc_value)
                if result > best_metric:
                    best_metric = result
                    best_metric_epoch = epoch + 1
                    torch.save(model.state_dict(), os.path.join(
                        root_dir, "best_metric_model.pth"))
                    # torch.save(model.state_dict(), os.path.join("C:\\Users\\NEUROPHET\\Desktop",
                    # "best_metric_model.pth"))
                    print("saved new best metric model")
                print(
                    f"current epoch: {epoch + 1} current AUC: {result:.4f}"
                    f" current accuracy: {acc_metric:.4f}"
                    f" best AUC: {best_metric:.4f}"
                    f" at epoch: {best_metric_epoch}"
                )

    print(
        f"train completed, best_metric: {best_metric:.4f} "
        f"at epoch: {best_metric_epoch}")

    # plt.figure("train", (12, 6))
    # plt.subplot(1, 2, 1)
    # plt.title("Epoch Average Loss")
    # x = [i + 1 for i in range(len(epoch_loss_values))]
    # y = epoch_loss_values
    # plt.xlabel("epoch")
    # plt.plot(x, y)
    # plt.subplot(1, 2, 2)
    # plt.title("Val AUC")
    # x = [val_interval * (i + 1) for i in range(len(metric_values))]
    # y = metric_values
    # plt.xlabel("epoch")
    # plt.plot(x, y)
    # plt.show()

    model.load_state_dict(torch.load(
        os.path.join(root_dir, "best_metric_model.pth")))
    model.eval()
    y_true = []
    y_pred = []
    with torch.no_grad():
        for test_data in test_loader:
            test_images, test_labels = (
                test_data[0].to(device),
                test_data[1].to(device),
            )
            pred = model(test_images).argmax(dim=1)
            for i in range(len(pred)):
                y_true.append(test_labels[i].item())
                y_pred.append(pred[i].item())

    print(classification_report(
        y_true, y_pred, target_names=class_names, digits=4))


# if directory is None:
#     shutil.rmtree(root_dir)
#     print("reove root_dir =>",root_dir)

if __name__ == "__main__":
    tutorial()
