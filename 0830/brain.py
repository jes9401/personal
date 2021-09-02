from collections import Counter

file = open("brain.txt", "r")
f = file.readlines()
file.close()
num_list = []
for i in f:
    num_list.extend(i.split(","))
num_list = list(map(lambda x: int(x.rstrip()), num_list))
num_list.sort()
num_dict = dict(Counter(num_list))

# 1
num_set_list = list(set(num_list))
num_set_list.sort()
print(num_set_list)

# 2
print(num_dict)
