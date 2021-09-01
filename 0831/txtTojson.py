import glob
import json
import os
import zipfile


def get_file_name(file):
    # \\를 기준으로 나눠서 파일이름만 저장
    file = file.split('\\')[-1]
    # *.txt 형태를 *.json 으로 변환
    file = file.split('.')[0]+".json"
    return file


def get_result(input_path, output_path):
    result = os.popen(".\\dist\\argparseTest\\argparseTest.exe --input_path {} --output_path {}".format(input_path, output_path)).read()
    # 실행 결과 중 2번째 값 저장
    result = result.split("\n")[1]
    # 딕셔너리 형태로 변환
    result = eval(result)
    return result


def create_file(file_name, result):
    # *.json 형태로 파일 생성한 뒤 내용에 결과 저장
    with open(file_name, 'w') as out_file:
        json.dump(result, out_file)


if __name__ == '__main__':
    # txt 파일들을 리스트에 저장
    in_path = "./brain/*.txt"
    out_path = "./brain_json/"
    txt_file = glob.glob(in_path)
    for i in txt_file:
        file_name = os.path.join(out_path, get_file_name(i))
        result = get_result(i, file_name)
