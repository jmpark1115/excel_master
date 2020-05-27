import sys
import csv
import pprint

'''

2) db 구조

tarding_min = 100 
botname = { 'FLATA-MTT' : ['FLATA-MTT', 'flata-mtt', ...],  .... }

bot_trade = { 'botname ' : flata-mtt, 'date' : { ['2020-05-27': 50회, 무효, ['2020-05-27':30회], ....  }
bot_trade_tot = [ bot_trade, .....]

3) 주요 로직

for name_k, name_v in botnames:
     if r.botname in name_v :
          bot_trade[name_k] =   

'''

URL = 'data/testdata1.csv'

config = { 'trading_min': 100, 'start' : '2020-05-25', 'end' : '2020-05-27'}
botnames = {
             'mtt-flata' : ['FLATA - MTT', 'flata - mtt'],
             'FLATA - BL' : ['FLATA - BL'],
             'FLATA - BLC' : ['FLATA - BLC'],
             'DPD - FLATA' : ['DPD - FLATA'],
             'KEYT-FLATA' : ['KEYT-FLATA'],
             'BITHUMB - LOA - BTC': ['BITHUMB - LOA - BTC'],
             'BITHUMB - LOA - USDT': ['BITHUMB - LOA - USDT'],
             'FLATA-NZC-2' : ['FLATA-NZC-2'],
             'WBF - BRX' : ['WBF - BRX'],
             'EXX - HUG' : ['EXX - HUG'],
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

for name_k, name_v in botnames.items():
    # 대표 botname 에 대해 거래량을 count 함
    cnt = 0
    bot = Bot(name_k)
    item = bot.getInstance()

    with open(URL, 'r', encoding='UTF-8') as f:
        reader = csv.DictReader(f, delimiter=',')

        for r in reader :
            print(r)
            if config['start'] <= r['create'][:10] <= config['end']:
                pass
            else:
                continue
            if r['botname'] in name_v:
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








