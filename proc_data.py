import csv
from datetime import datetime, timedelta

# URL = 'data/testdata1.csv'
# URL = 'data/export_0527_bserver.csv'
URL = 'data/export_abc_server_0527.csv'

config = { 'trading_min': 100,
           'start' : '2020-04-01',
           'end' : '2020-05-31',
           'incentive' : 70/31,
           'username' : 'bos992'
          }

botnames = {
            'ua-coinsbit' : {'name': ['UA-COINSBIT', 'UA-COINSBIT2']},
            'keyt-flata': {'name': ['KEYT-FLATA'], },
            'dpd-flata': {'name': ['DPD - FLATA', 'DPD-FLATA']},
            'loa-btc-bithumb': {'name': ['BITHUMB - LOA - BTC', 'LOA-BTC-BITHUMBPRO'],},
            'loa-usdt-bithumb': {'name': ['BITHUMB - LOA - USDT', 'LOA-BITHUMBPRO'], 'start': '2020-04-20', 'end': '2020-05-30'},
            'zg-brx': {'name': ['ZG - BRX'], 'start': '2020-05-17', 'end': '2020-05-31'},
            'nzc-flata': {'name': ['FLATA-NZC-2', 'FLATA - NZC', 'NZC-FLATA'], 'start': '2020-05-14', 'end': '2020-05-31'},
            'brx-wbf' : {'name' : ['WBF - BRX'], 'start': '2020-05-07', 'end': '2020-05-31'},
            'mtt-flata': {'name': ['FLATA - MTT', 'MTT-FLATA', 'flata - mtt'], 'start': '2020-05-06', 'end': '2020-05-31'},
            'blc-flata': {'name': ['FLATA - BLC', 'BLC-FLATA'], 'start': '2020-05-06', 'end': '2020-05-31'},
            'bl-flata': {'name': ['FLATA - BL', 'BL-FLATA'], 'start': '2020-05-06', 'end': '2020-05-31'},
            'hug-exx' : {'name' : ['EXX - HUG'], 'start': '2020-05-06', 'end': '2020-05-31'},
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
            if start_date <= r['create'][:10] <= end_date :
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








