import argparse
parser = argparse.ArgumentParser()

parser.add_argument('--path')
args = parser.parse_args()

try:
    file = open(args.path, 'r')
    f = file.readlines()
    file.close()
    num_list = []
    num_dic = {}

    # 모든 숫자 num_list에 추가 후 정수형으로 변경(정렬 위함)
    for i in f:
        num_list.extend(i.split(","))
    num_list = list(map(lambda x: int(x.rstrip()), num_list))
    num_list.sort()

    # num_dic에 숫자가 없으면 새로 생성(초기값 1)
    # 있을 경우 값 +1
    for x in num_list:
        if x in num_dic:
            num_dic[x] += 1
        else:
            num_dic[x] = 1

    num_set_list = list(set(num_list))
    num_set_list.sort()
    print("{}".format(num_set_list))

    print(num_dic)
except Exception as e:
    print(e)
