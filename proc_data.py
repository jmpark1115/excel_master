import csv
from datetime import datetime, timedelta

'''
사용법
1. 사이트에서 DB 백업데이터를 다운로드
2. 그대로 EXCEL MASTER 디렉토리 해당월로 만든후
3. 해당 파일이름과 URL 을 일치
4. config 에서 start ~ end 날짜, incentive 월을 수정
5. 실행
'''
'''
DB 만드는 법
use obs_1230;
show tables;
select count(*) from sitetrading_trans;
select * from sitetrading_trans into outfile "C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\trans_bserver03.csv" fields terminated by ',' lines terminated by '\n';
header name 이 없으므로 명기함.
30일 말일까지 있는지 확인
'''

# URL = 'data12/trans_cserver.csv'
URL = 'data12/trans_bserver03.csv'

config = { 'trading_min': 10,
           'start' : '2020-12-01',
           'end' : '2020-12-31',
           'incentive' : 70/31,
           'username' : 'bos992'
          }

botnames = {
            'qpbio-flata'    : {'name':['FLATA-QPBIO']},
            'gdt-foblgate'   : {'name':['GDT-FOBLGATE']},
            'kvdc-foblgate'  : {'name':['KVDC-FOBLGATE']},

            'hgn-probit'     : {'name':['HGN-PROBIT', 'HGN-PROBIT2']},
            'hgn-flata'      : {'name':['HGN-FLATA']},
            'csp-foblgate'   : {'name':['CSP-FOBLGATE']},
            'qpbio-foblgate' : {'name':['QPBIO-FOBLGATE']},
            'lot-foblgate'  : {'name':['LOT-FOBLGATE']},
            'mtrax-latoken'  : {'name':['MTRAX-LATOKEN']},
            'mccx-dcoin'  : {'name':['MCCX-DCOIN']},
            'kful-flata'  : {'name': ['KFUL-FLATA']},
            # 'gbk-bibox'   : {'name': ['GBK-BIBOX']},
            # 'sw-foblgate' : {'name': ['SW-FOBLGATE']},
            # 'ua-coinsbit' : {'name': ['UA-COINSBIT', 'UA-COINSBIT2']},
            'keyt-flata': {'name': ['KEYT-FLATA'], },
            # 'dpd-flata': {'name': ['DPD - FLATA', 'DPD-FLATA']},
            'loa-btc-bithumb': {'name': ['BITHUMB - LOA - BTC', 'LOA-BTC-BITHUMBPRO'],},
            'loa-usdt-bithumb': {'name': ['BITHUMB - LOA - USDT', 'LOA-BITHUMBPRO'], },
            # 'zg-brx': {'name': ['ZG - BRX'], },
            # 'nzc-flata': {'name': ['FLATA-NZC-2', 'FLATA - NZC', 'NZC-FLATA'], },
            # 'brx-wbf' : {'name' : ['WBF - BRX'], },
            'mtt-flata': {'name': ['FLATA - MTT', 'MTT-FLATA', 'flata - mtt'], },
            'blc-flata': {'name': ['FLATA - BLC', 'BLC-FLATA'],},
            'bl-flata': {'name': ['FLATA - BL', 'BL-FLATA'],},
            # 'hug-exx' : {'name' : ['EXX - HUG', 'HUG-EXX'], },
           }


bot_t = list()
item = dict()

class Bot(object):
    def __init__(self, botname):
        self.bot = {
            'botname' : botname,
            'date' : {}
        }

    def getInstance(self):
        return self.bot


def report(bots):

    tot_incentive = 0
    csvfile = 'data/result_{}.csv' .format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    filename = csvfile

    with open(filename, 'w', encoding='cp949', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow('')

        for i, bot in enumerate(bots):

            # print(bot['botname'])

            result = sorted(bot['date'].items())
            bot['date'] = result
            start_date = bot['date'][0][0] if bot['date'] else None
            end_date   = bot['date'][-1][0] if bot['date'] else None
            print('%d. %s' % (i+1, bot['botname']))
            print('date range : {} ~ {}' .format(start_date, end_date))

            writer.writerow(['%d. %s' % (i, bot['botname'])])
            writer.writerow(['date range : {} ~ {}'.format(start_date, end_date)])

            result = list()
            cnt  = tot_cnt = 0
            for date in bot['date']:
                result.append("%s(%d)" %(date[0][-5:], date[1]))
                if date[1] >= config['trading_min']:
                    cnt += 1
                tot_cnt += 1
            incentive = config['incentive']*cnt
            tot_incentive += incentive
            print('total operation date : ', ','.join(result))
            print('total validity date : %d/%d'% (cnt, tot_cnt))
            print('incentive {:.4f} won' .format(incentive))
            writer.writerow(['total operation date : %s' % ','.join(result)])
            writer.writerow(['total validity date : %d/%d'% (cnt, tot_cnt)])
            writer.writerow(['incentive {:.4f} won' .format(incentive)])

        print('==================================================')
        print('incentive per date {:.8f} won' .format(config['incentive']))
        print('total incentive {:.4f} won' .format(tot_incentive))
        writer.writerow('[==================================================]')
        writer.writerow(['incentive per date {:.8f} won' .format(config['incentive'])])
        writer.writerow(['total incentive {:.4f} won' .format(tot_incentive)])

for name_k, name_v in botnames.items():
    # 대표 botname 에 대해 거래량을 count 함
    cnt = 0
    bot = Bot(name_k)
    item = bot.getInstance()

    with open(URL, 'r', encoding='UTF-8') as f:
        reader = csv.DictReader(f, delimiter=',')

        if 'start' in name_v :
            start_date = name_v['start']
            end_date   = name_v['end']
        else:
            start_date = config['start']
            end_date   = config['end']
        for r in reader :
            # print(r)
            if r['username'] != config['username']:
                continue
            #jmpark
            # if start_date <= r['create'][:10] <= end_date :
            if start_date <= r['create'] <= end_date :
                    pass
            else:
                continue
            if r['botname'] in name_v['name']:
                date = r['create'][:10]
                # key 확인
                if date in item['date'].keys():
                    item['date'][date] += 1
                else:
                    item['date'][date] = 1

        # print(item)
        bot_t.append(item)

report(bot_t)








