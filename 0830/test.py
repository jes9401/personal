file = open("brain.txt", "r")
f = file.readlines()

num_list = []
num_dic = {}

for i in f:
    num_list.extend(i.split(","))
num_list = list(map(lambda x: int(x.rstrip()), num_list))
num_list.sort()

for x in num_list:
    if x in num_dic:
        num_dic[x] += 1
    else:
        num_dic[x] = 1

# 1
num_set_list = list(set(num_list))
num_set_list.sort()
print(num_set_list)

# 2
for y in num_dic:
    print("{} => {}개".format(y, num_dic[y]))
