import datetime
import threading
import time

from ibapi import wrapper
from ibapi.client import EClient
from ibapi.common import BarData, ListOfHistoricalSessions, SetOfString, SetOfFloat
from ibapi.contract import Contract

"""
参考
https://algotrading101.com/learn/interactive-brokers-python-api-native-guide/
https://interactivebrokers.github.io/tws-api/basic_contracts.html#opt

需要花钱订阅数据：https://ibkr.info/article/2840
"""

class TestWrapper(wrapper.EWrapper):
    pass


class TestClient(EClient):
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)


class TestApp(TestWrapper, TestClient):
    def __init__(self):
        self.tickid=0
        TestWrapper.__init__(self)
        TestClient.__init__(self, wrapper=self)

    def get_contract(self, symbol):
        contract = Contract()
        contract.symbol = symbol # "SPY 230120C00398000"
        contract.secType = "OPT"
        contract.exchange = "SMART"
        # contract.primaryExchange = "ISLAND"
        contract.currency = "USD"
        contract.lastTradeDateOrContractMonth = "20230330" # "JAN23"
        contract.strike = 398
        contract.right = "C"
        contract.multiplier = "100"
        contract.tradingClass = 'SPY'
        return contract

    def get_contract4chain(self, symbol):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = "OPT"
        contract.exchange = "SMART"
        contract.currency = "USD"
        contract.lastTradeDateOrContractMonth = "20230330"
        # contract.strike = 398
        """
        20230330 * (3500~4500)
        20230318 * (3500~4500)
        3.30,
              4.1,4.2,4.5,4.7,4.8 date
              3790 ~ 4100
              4.1 (3790 ~ 4100) contract, 每分钟3.30，1次调用
              4.2
        4.1
              4.2, 4.3, 4.5, 4.7, 4.9
              3810~ 4100
'''
        3-30-4-1-C-4100.csv
        3-30-4-1-C-4200.csv
        3-30-4-1-C-4300.csv # 1天的数据，7x60 = 420                
'''
"""
        contract.right = "C"
        contract.multiplier = "100"
        contract.tradingClass = symbol
        return contract

    def get_option_chain(self, symbol):
        # https://interactivebrokers.github.io/tws-api/options.html
        # data = self.reqContractDetails(213, self.get_contract4chain(symbol))

        # 上面的方法总返回None，试试这个：
        # https://interactivebrokers.github.io/tws-api/classIBApi_1_1EClient.html#adb17b291044d2f8dcca5169b2c6fd690

        # app.reqSecDefOptParams(0, contract.symbol, "", contract.secType, contract.conId)
        contract = Contract()
        contract.symbol = "SPX"
        contract.secType = "IND"
        contract.exchange = "CBOE"
        contract.currency = "USD"
        app.reqContractDetails(0, contract)

        data = self.reqSecDefOptParams(100,symbol,"","OPT",contract.conId)
        return data

    def contractDetails(self, reqId, contractDetails):
        self.contract_details = contractDetails

    def contractDetailsEnd(self, reqId):
        super().contractDetailsEnd(reqId)
        print("Contract details received.")

    def securityDefinitionOptionParameter(self, reqId:int, exchange:str, underlyingConId:int, tradingClass:str,
                                          multiplier:str, expirations:SetOfString, strikes:SetOfFloat):
        print(f"Option chain parameters received for reqId {reqId}:\n"
              f"Exchange: {exchange}\n"
              f"Underlying conId: {underlyingConId}\n"
              f"Trading class: {tradingClass}\n"
              f"Multiplier: {multiplier}\n"
              f"Expirations: {expirations}\n"
              f"Strikes: {strikes}")

    def get_option(self, symbol):
        """
        IBApi.EClient.reqHistoricalData function. Every request needs:
        ---------------------------------------------------------------
        tickerId, A unique identifier which will serve to identify the incoming data.
        contract, The IBApi.Contract you are interested in.
        endDateTime, The request's end date and time (the empty string indicates current present moment).
        durationString, The amount of time (or Valid Duration String units) to go back from the request's given end date and time.
        barSizeSetting, The data's granularity or Valid Bar Sizes
        whatToShow, The type of data to retrieve. See Historical Data Types
        useRTH, Whether (1) or not (0) to retrieve data generated only within Regular Trading Hours (RTH)
        formatDate, The format in which the incoming bars' date should be presented. Note that for day bars, only yyyyMMdd format is available.
        keepUpToDate, Whether a subscription is made to return updates of unfinished real time bars as they are available (True), or all data is returned on a one-time basis (False). Available starting with API v973.03+ and TWS v965+. If True, and endDateTime cannot be specified.
        """
        contract = self.get_contract(symbol)

        # 今天往前10天的数据
        queryTime = (datetime.datetime.today() - datetime.timedelta(days=10)).strftime("%Y%m%d-%H:%M:%S")
        # queryTime = datetime.datetime.today()
        print("begin to query")
        self.reqHistoricalData(reqId=self.tickid, # 序列号，递增就可以
                               contract=contract, # contract对象，需要在其肚子里指定期权信息，从而确定合约名
                               endDateTime=queryTime,
                               durationStr="1 M", # 分钟级数据
                               barSizeSetting="30 mins", #
                               whatToShow="TRADES",#"MIDPOINT",
                               useRTH=1,
                               formatDate=1,
                               keepUpToDate=False,
                               chartOptions=[])

        print("after query")

    def get_stock(self,symbol):
        # Create contract object
        contract = Contract()
        contract.symbol = symbol
        contract.secType = 'STK'
        contract.exchange = 'SMART'
        contract.primaryExchange = "ISLAND"
        contract.currency = 'USD'

        # Request Market Data
        app.reqHistoricalData(self.tickid, contract, '', '2 D', '1 hour', 'BID', 0, 2, False, [])

    def get_eur(self):
        eurusd_contract = Contract()
        eurusd_contract.symbol = 'EUR'
        eurusd_contract.secType = 'CASH'
        eurusd_contract.exchange = 'IDEALPRO'
        eurusd_contract.currency = 'USD'
        # Request historical candles
        app.reqHistoricalData(self.tickid, eurusd_contract, '', '2 D', '1 hour', 'BID', 0, 2, False, [])

    def historicalData(self, reqId: int, bar: BarData):
        print(f"获得数据[{reqId}]:{bar}")

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        super().historicalDataEnd(reqId, start, end)
        print("HistoricalDataEnd. ReqId:", reqId, "from", start, "to", end)

    def historicalDataUpdate(self, reqId: int, bar: BarData):
        print("HistoricalDataUpdate. ReqId:", reqId, "BarData.", bar)

    def historicalSchedule(self, reqId: int, startDateTime: str, endDateTime: str, timeZone: str,
                           sessions: ListOfHistoricalSessions):
        super().historicalSchedule(reqId, startDateTime, endDateTime, timeZone, sessions)
        print("HistoricalSchedule. ReqId:", reqId, "Start:", startDateTime, "End:", endDateTime, "TimeZone:",
              timeZone)

        for session in sessions:
            print("\tSession. Start:", session.startDateTime, "End:", session.endDateTime, "Ref Date:",
                  session.refDate)


app = TestApp()

def run():
    app.connect("127.0.0.1", 7496, clientId=0)
    print("connect ok!")
    app.run()
    print("application ran!")


# python main.py
if __name__ == '__main__':
    api_thread = threading.Thread(target=run, daemon=True)
    api_thread.start()
    time.sleep(3)

    # print("-" * 80)
    # print("获取外币数据")
    # app.get_eur()
    # time.sleep(3)
    #
    # print("-" * 80)
    # print("获取股票数据")
    # app.tickid+=1
    # app.get_stock('AAPL')
    # time.sleep(3)


    print("-"*80)
    print("获取期权数据")
    app.tickid += 1
    print(f"Contacts:{app.reqContractDetails(app.tickid,app.get_contract('SPY 230330C00379000'))}")
    app.tickid += 1
    app.get_option('SPX')
    time.sleep(3)  # sleep to allow enough time for data to be returned

    # 获得期权链
    # data = app.get_option_chain('SPX')
    # print("获得SPY的option chain：")
    # print(data)
    #
    # time.sleep(30)

    app.disconnect()
    print("sent query")


"""
Historical Market Data Service error message:No market data permissions for AMEX OPT
Historical Market Data Service error message:No data of type EODChart is available for the exchange 'BEST' and the security type 'Option' and '1 m' and '1 day'
The contract description specified for SPY 230120C00384000 is ambiguous.
Historical Market Data Service error message:No market data permissions for ISLAND STK. Requested market data requires additional subscription for API. See link in 'Market Data Connections' dialog for more details.
"""