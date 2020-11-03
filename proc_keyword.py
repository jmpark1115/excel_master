# 출처: https://3months.tistory.com/203 [Deep Play]

from datetime import datetime, timedelta
from os import listdir
from os.path import isfile, join
import sys

filepath = 'logs1103_2'   # 대표의 리포트 요청
# filepath = 'logs1103_3'  #  해커공격 신고

files = [f for f in listdir(filepath) if isfile(join(filepath, f))]
files = [x for x in files if x.find("logfile") != -1]

file_w = filepath + '/result_{}.txt'.format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
keyword = '!!!'

with open(file_w, 'a', encoding='utf-8') as fw:
    tot = 0
    for file in files:
        fw.write(file)
        fw.write('\n')
        sum = 0
        with open(join(filepath, file), 'r', encoding='utf-8') as fr:
            while True:
                line = fr.readline()
                if not line:
                    break
                if keyword in line:
                    print(line)
                    fw.write(line)
                    sum += 1
            fw.write(f'SUM = {sum}\n')
            tot += sum

    fw.write(f'TOT = {tot}\n')
    fw.write('end of file')
