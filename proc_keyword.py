# 출처: https://3months.tistory.com/203 [Deep Play]

from datetime import datetime, timedelta
from os import listdir
from os.path import isfile, join
import sys

# filepath = 'logs1103_2'   # 대표의 리포트 요청
# filepath = 'logs1103_3'  #  해커공격 신고
# filepath = 'logs1104_1'    # retry cancel error
#filepath = 'C:\\Users\\jmpark\\Desktop\\MyLogs\\RT7\\1108_mysql'
# filepath = 'C:\\Users\\jmpark\\Desktop\\mylogs\BOS\\1109_c_2'
# filepath = 'C:\\Users\\jmpark\\Desktop\\mylogs\BOS\\1110_b'
# filepath = 'C:\\Users\\jmpark\\Desktop\\mylogs\BOS\\1111_c'
# filepath = 'C:\\Users\\jmpark\\Desktop\\mylogs\BOS\\1112_b'
# filepath = 'C:\\Users\\jmpark\\Desktop\\mylogs\BOS\\1112_c'
# filepath = 'C:\\Users\\jmpark\\Desktop\\mylogs\BOS\\1207'
# filepath = 'C:\\Users\\jmpark\\Desktop\\mylogs\BOS\\1207_2'
# filepath = 'C:\\Users\\jmpark\\Desktop\\mylogs\BOS\\1213_01'
# filepath = 'C:\\Users\\jmpark\\Desktop\\mylogs\BOS\\1223'
# filepath = 'C:\\Users\\jmpark\\Desktop\\mylogs\BOS\\1231'
# filepath = 'C:\\Users\\jmpark\\Desktop\\mylogs\BOS\\2021년\\0107'
# filepath = 'C:\\Users\\jmpark\\Desktop\\mylogs\\Dvc\\0113'
# filepath = 'C:\\Users\\jmpark\\Desktop\\mylogs\\Swapp\\210118'
# filepath = 'C:\\Users\\jmpark\\Desktop\\mylogs\\duru\\210117'
# filepath = 'C:\\Users\\jmpark\\Desktop\\mylogs\\swapp\\210122'
filepath = 'C:\\Users\\jmpark\\Desktop\\mylogs\\BOS\\2021년\\0201'

files = [f for f in listdir(filepath) if isfile(join(filepath, f))]
# files = [x for x in files if x.find("logfile") != -1]
files = [x for x in files if x.find("orderbook") != -1]
print(files)
file_w = filepath + '/result_{}.txt'.format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
# keyword = '!!!'
# keyword = 'cancel false reason:'
# keyword = 'Retry cancel success !:'
# keyword = 'partially'
# keyword = 'db_handling error'
# keyword = '!!! Found Hacker'
# keyword = '84@184'
# keyword = 'cancel false reason'
# keyword = 'response error'
# keyword = 'Retry cancel fail'
keyword = 'Exception'
# keyword = 'Not enough credits'
# keyword = 'ids'
# keyword = 'Error'


with open(file_w, 'a', encoding='utf-8') as fw:
    tot = 0
    for file in files:
        fw.write(file)
        print(file)
        fw.write('\n')
        sum = 0
        no  = 0
        with open(join(filepath, file), 'r', encoding='utf-8') as fr:
            prev_line = ''
            while True:
                line = fr.readline()
                no += 1
                if not line:
                    break
                if keyword.lower() in line.lower() :
                    print(f'({no-1}) ' +prev_line)
                    print(f'({no}) ' +line)
                    fw.write(f'({no-1}) ' +prev_line)
                    fw.write(f'({no}) ' +line)
                    sum += 1
                prev_line = line
            fw.write(f'SUM = {sum}\n')
            tot += sum

    fw.write(f'TOT = {tot}\n')
    fw.write('end of file')
