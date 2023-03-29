import threading
import time

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.common import *
from ibapi.contract import ContractDetails
from ibapi.tag_value import TagValue


class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.contract_details = None

    def error(self, reqId, errorCode, errorString,json):
        print(f"Error: {reqId} {errorCode} {errorString} {json}")

    def contractDetails(self, reqId, contractDetails):
        self.contract_details = contractDetails
        print("回调：contractDetails",contractDetails)

    def contractDetailsEnd(self, reqId):
        super().contractDetailsEnd(reqId)
        print("Contract details received.")

    def securityDefinitionOptionParameter(self, reqId: int, exchange: str, underlyingConId: int, tradingClass: str,
                                          multiplier: str, expirations: SetOfString, strikes: SetOfFloat):
        print(f"Option chain parameters received for reqId {reqId}:\n"
              f"Exchange: {exchange}\n"
              f"Underlying conId: {underlyingConId}\n"
              f"Trading class: {tradingClass}\n"
              f"Multiplier: {multiplier}\n"
              f"Expirations: {expirations}\n"
              f"Strikes: {strikes}")


def run():
    app.connect("127.0.0.1", 7496, clientId=0)
    print("connect ok!")
    app.run()


def main():
    contract = Contract()

    contract.symbol = "SPX"
    contract.secType = "IND"
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.multiplier = "100"
    contract.exchange = "CBOE"

    # contract.symbol = "AAPL"
    # contract.secType = "STK"
    # contract.exchange = "SMART"
    # contract.currency = "USD"

    # IBM的例子：参考https://interactivebrokers.github.io/tws-api/options.html#option_chains
    # 必须conID是8314，secType是STK
    # contract.symbol = "IBM"
    # contract.secType = "STK"
    # contract.exchange = "SMART"
    # contract.currency = "USD"
    # contract.conId = 8314


    # 通过reqContractDetails获得期权链数据
    app.reqContractDetails(0, contract)
    print("请求：reqContractDetails")
    while app.contract_details is None:
        time.sleep(3)
        print(".")
    print("获得contract_details")

    # 通过reqSecDefOptParams获得期权链数据
    print("请求：reqSecDefOptParams")
    contract_details = app.contract_details
    app.reqSecDefOptParams(1,contract_details.contract.symbol ,
                           "",
                           contract_details.contract.secType,
                           contract_details.contract.conId)


# python get_option_chain_by_ib_sync.py
if __name__ == '__main__':
    app = TestApp()

    api_thread = threading.Thread(target=run, daemon=True)
    api_thread.start()
    time.sleep(3)

    main()
    while True:
        time.sleep(1)
