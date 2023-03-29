# https://nbviewer.org/github/erdewit/ib_insync/blob/master/notebooks/option_chain.ipynb
from ib_insync import *
util.startLoop()


ib = IB()
ib.connect('127.0.0.1', 7496, clientId=12)

spx = Index('SPX', 'CBOE')
ib.qualifyContracts(spx)

# ib.reqMarketDataType(4)

# [ticker] = ib.reqTickers(spx)
# print(ticker)

chains = ib.reqSecDefOptParams(spx.symbol, '', spx.secType, spx.conId)
# import pdb;pdb.set_trace()
df = util.df(chains)
print(df.expirations[0])
print(df.strikes[0])

# python get_option_chain_by_ib_sync.py

