import glob
import json
import os
import shutil
import zipfile

# brain 폴더 생성
if not os.path.exists('./brain'):
    os.makedirs('./brain')

# brain.zip 파일을 brain 폴더에 압축 해제
zipfile.ZipFile('brain.zip').extractall('./brain')
# json 파일 압축할 zip 파일 생성
json_zip = zipfile.ZipFile('brain_json.zip', 'w')
# 압축해제 한 txt 파일들을 리스트에 저장
txt_file = glob.glob('./brain/*.txt')

for i in range(len(txt_file)):
    temp = txt_file[i]
    result = os.popen("dist\\argparseTest.exe --path "+temp).read()
    # 실행 결과 중 2번째 값만 저장
    result = result.split("\n")[1]
    # 딕셔너리 형태로 변환
    result = eval(result)
    # \\를 기준으로 나눠서 파일이름만 저장
    file_name = txt_file[i].split('\\')[-1]
    # *.txt 형태를 *.json 으로 변환
    file_name = file_name.split('.')[0]+".json"
    
    # *.json 형태로 파일 생성한 뒤 내용에 결과 저장
    with open(file_name, 'w') as outfile:
        json.dump(result, outfile)
    # 압축 파일에 추가하고 추가된 파일은 삭제
    json_zip.write(file_name)
    os.remove(file_name)
json_zip.close()
shutil.rmtree("brain")
