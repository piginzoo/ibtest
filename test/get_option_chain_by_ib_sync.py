# https://nbviewer.org/github/erdewit/ib_insync/blob/master/notebooks/option_chain.ipynb
import os.path

from ib_insync import *
util.startLoop()


ib = IB()
ib.connect('127.0.0.1', 7496, clientId=12)

# spx = Index('SPX', 'CBOE')
spx = Option('SPX', '', 0, 'C',  'CBOE', 100, 'USD')

opt_list = ib.qualifyContracts(spx)

# ib.reqMarketDataType(4)

# [ticker] = ib.reqTickers(spx)
# print(ticker)
import pdb;pdb.set_trace()

chains = ib.reqSecDefOptParams(spx.symbol, '', spx.secType, spx.conId)
# import pdb;pdb.set_trace()

df = util.df(chains)
df.to_csv('data/spx.csv')
# python get_option_chain_by_ib_sync.py

def get_trade_dates():
    pass


def get_spx_scope(day,date_list,spx_data):
    """
    获得 day 之后7天的spx的范围
    :param day:
    :return:
    """
    index = date_list.find(day)
    seven_days = date_list[index:index+7]
    max_high = max_low = -1
    for day in seven_days:
        high = spx_data[day].high
        low =  spx_data[day].low
        if high>max_high: max_high = high
        if low < min_low: min_low = low
    return max_low,max_high,sever_days

def download(day,expoir,strike):
    # 获取 SPX 的合约
    contract = Option(f'SPX{expire}{strike}', 'CBOE')

    # 创建历史数据请求
    bars = ib.reqHistoricalData(
        contract=contract,
        endDateTime='',
        durationStr='1 D',
        barSizeSetting='1 min',
        whatToShow='TRADES',
        useRTH=True
    )
    return bars

    # 从2022-1-1 到今天
    date_list = get_trade_dates()


    for day in date_list:

        scope, seven_days = get_spx_scope(day)

        for point in scope: # 3853 ~ 4122
            for expire in seven_days:
                name = f"{day}-{point}-{expire}.csv"
                if os.path.exists(name): continue
                df = download(day,point,expire)
                df.to_csv(name)

