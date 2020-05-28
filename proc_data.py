import sys, os
import csv
from datetime import datetime, timedelta

'''

2) db 구조

tarding_min = 100 
botname = { 'FLATA-MTT' : ['FLATA-MTT', 'flata-mtt', ...],  .... }

bot_trade = { 'botname ' : flata-mtt, 'date' : { '2020-05-27': 50, '2020-05-27':30, ....  }
bot_trade_tot = [ bot_trade, .....]

3) 주요 로직

for name_k, name_v in botnames:
     if r.botname in name_v :
          bot_trade[name_k] =   

'''

URL = 'data/testdata1.csv'

config = { 'trading_min': 3,
           'start' : '2020-05-25',
           'end' : '2020-05-27',
           'incentive' : 70/30
          }

botnames = {
             'mtt-flata' : {'name' : ['FLATA - MTT', 'flata - mtt'], 'start': '2020-05-30', 'end': '2020-05-31'},
             'FLATA - BL' : {'name' : ['FLATA - BL'],},
             'FLATA - BLC' : {'name' : ['FLATA - BLC'],},
             'DPD - FLATA' : {'name' : ['DPD - FLATA'],},
             'KEYT-FLATA' : {'name' : ['KEYT-FLATA'],},
             'BITHUMB - LOA - BTC': {'name': ['BITHUMB - LOA - BTC'],},
             'BITHUMB - LOA - USDT': {'name' : ['BITHUMB - LOA - USDT'],},
             'FLATA-NZC-2' : {'name' : ['FLATA-NZC-2'],},
             'WBF - BRX' : {'name' : ['WBF - BRX'], },
             'EXX - HUG' : {'name' : ['EXX - HUG'], },
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
    current_datetime = datetime.now()
    csvfile = 'data/result_{}.csv' .format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    # filename = os.path.join('data' , csvfile)
    filename = csvfile

    with open(filename, 'w', encoding='cp949', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow('')

        for i, bot in enumerate(bots):

            result = sorted(bot['date'].items())
            bot['date'] = result
            result = []
            for r in bot['date'] :
                result.append(list(r))

            bot['date'] = result
            for date in bot['date']:
                if date[1] < config['trading_min']:
                    date.append(False)
                else:
                    date.append(True)
            start_date = bot['date'][0][0] if bot['date'] else None
            end_date   = bot['date'][-1][0] if bot['date'] else None
            print('%d. %s' % (i, bot['botname']))
            print('date range : {} ~ {}' .format(start_date, end_date))

            writer.writerow(['%d. %s' % (i, bot['botname'])])
            writer.writerow(['date range : {} ~ {}'.format(start_date, end_date)])

            result = list()
            cnt  = 0
            for date in bot['date']:
                result.append("%s(%d)" %(date[0][-2:], date[1]))
                if date[2] == True:
                    cnt += 1
            incentive = config['incentive']*cnt
            tot_incentive += incentive
            print('total operation date : ', ','.join(result))
            print('total validity date : %d'% cnt)
            print('incentive {:.4f} won' .format(incentive))
            writer.writerow(['total operation date : %s' % ','.join(result)])
            writer.writerow(['total validity date : %d'% cnt])
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
            if start_date <= r['create'][:10] <= end_date:
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

for bot in bot_t:
    print(bot)

report(bot_t)







