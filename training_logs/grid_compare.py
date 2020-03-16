import os
import sys
import re

def add_to_dic(dic, name, line):
    match  = re.match(r'(([a-z]+-)+)(0\.\d+-0\.\d+)' , name)
    groups = match.groups()
    config = groups[0]
    params = groups[-1]
    l = line.split()
    epoch = l[5]
    score = float(l[-1])
    if (config in dic and score > dic[config][2]) or config not in dic:
        dic[config] = (params, epoch,  score)

dic = {}

for root, dirs, files in os.walk(sys.argv[1]):
   for name in files:
      with open(os.path.join(root, name), 'r') as f:
          add_to_dic(dic, name, f.readlines()[-1].strip())

print(dic)