from collections import Counter
import argparse
from txtTojson import create_file

parser = argparse.ArgumentParser()
parser.add_argument('--input_path')
parser.add_argument('--output_path')
args = parser.parse_args()

try:
    file = open(args.input_path, 'r')
    f = file.readlines()
    file.close()
    num_list = []

    # 모든 숫자 num_list에 추가 후 정수형으로 변경(정렬 위함)
    for i in f:
        num_list.extend(i.split(","))
    num_list = list(map(lambda x: int(x.rstrip()), num_list))
    num_list.sort()
    num_set_list = list(set(num_list))
    num_set_list.sort()
    num_dict = dict(Counter(num_list))
    print(num_set_list)
    print(num_dict)

    create_file(args.output_path, num_dict)
except Exception as e:
    print(e)
