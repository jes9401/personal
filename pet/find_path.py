import pandas as pd
from glob import glob
from datetime import datetime


# 하위 파일 리스트 반환 함수
def get_file_list(path):
    return glob(r"{}\*".format(path))


if __name__ == "__main__":
    # 드라이버에 맞게 수정
    total_list = glob(r"Z:\Img_Opensource\nii\ADNI_MRI_PET_pair\*")
    data_list = []
    for i in total_list:
        id_date_list = get_file_list(i)
        u_id = i.split("\\")[-1]
        t1_list = []

        # 같은 id 내에 하위 폴더들을 돌면서 리스트에 t1 데이터 추가(경로, 시간)
        for j in id_date_list:
            id_date_mri_list = get_file_list(j)
            for k in id_date_mri_list:
                if "t1" in k.split("\\")[-1]:
                    t1_dict = {"t1_path": get_file_list(k)[0], "t1_date": k.split("\\")[-2].split("_")[-1]}
                    t1_list.append(t1_dict)

        for l in id_date_list:
            id_date_mri_list = get_file_list(l)
            # id_date_mri_list pet 폴더가 없는 경우 다음 루프로 넘어감
            pet_check = list(map(lambda x: "pet" in x.split("\\")[-1], id_date_mri_list))
            if pet_check.count(True) == 0:
                continue
            # pet 폴더가 있는 경우
            else:
                t1_path = None
                t1_date = None
                # pet_check 리스트 인덱스 값이 True => pet 폴더
                pet_path = id_date_mri_list[pet_check.index(True)]
                pet_path = get_file_list(pet_path)[0]
                # 파일 이름 형식이 다른 경우가 1가지만 있어서 if문으로 처리함
                if "2018-09-24_15_27_20.0" in pet_path:
                    pet_date = "20180924"
                else:
                    # 폴더명에서 date 추출
                    pet_date = pet_path.split("\\")[-3].split("_")[-1]

                # mri 폴더 중에 t1 폴더가 있으면 t1_path와 t1_date 값 할당
                for m in id_date_mri_list:
                    if "t1" in m:
                        t1_path = get_file_list(m)[0]
                        t1_date = m.split("\\")[-2].split("_")[-1]
                # 반복문 수행 후 t1_path 와 t1_date 값이 None이면 같은 id 내의 다른 폴더에서 가져옴
                if t1_path is None:
                    # 다른 폴더 내에도 t1 폴더가 없을 경우
                    if len(t1_list) == 0:
                        gap = None
                        pass
                    else:
                        # pet_date와의 차이를 계산
                        time_check = list(map(lambda x: abs(
                            datetime.strptime(pet_date, '%Y%m%d') - datetime.strptime(x["t1_date"], '%Y%m%d')), t1_list))
                        # 가장 차이가 적은 t1 폴더의 경로와 시간 할당
                        index = time_check.index(min(time_check))
                        t1_path = t1_list[index]["t1_path"]
                        t1_date = t1_list[index]["t1_date"]
                        gap = datetime.strptime(pet_date, '%Y%m%d') - datetime.strptime(t1_date, '%Y%m%d')
                else:
                    gap = datetime.strptime(pet_date, '%Y%m%d') - datetime.strptime(t1_date, '%Y%m%d')
                data_list.append([u_id, t1_path, pet_path, t1_date, pet_date, gap])

    # list -> dataframe
    df = pd.DataFrame(data_list, columns=['id', 't1_path', 'pet_path', 't1_date', 'pet_date', 'gap'])
    df.to_csv("result.csv", index=False)