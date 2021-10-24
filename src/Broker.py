
from coinbase.wallet.client import Client
from dateutil import parser
import datetime
import pytz
import logging
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# set API created on Coinbase
API_KEY = os.environ.get('API_KEY', None)
API_SECRET = os.environ.get('API_SECRET', None)


class Broker:

    def __init__(self):
        logger.info("Create broker")
        self.__client = Client(API_KEY, API_SECRET)
        # set threshold param
        self.__CURRENCY_EXCHANGE = 'EUR'
        self.__DESIRED_EARN = 20
        # create wallet of crypto and buy price
        self.UpdateWallet()

    def UpdateWallet(self):
        # update list crypto
        self.__walletDict = {}
        for x in self.__client.get_accounts().data:
            # check if there is amount and if is different of currency exchange
            if float(x.balance.amount) > 0 and x.balance.currency != self.__CURRENCY_EXCHANGE:
                self.__walletDict[x.balance.currency] = 0

        # update amount crypto
        for cryptoID in self.__walletDict:
            last_sell_found = False
            for trans in self.__client.get_transactions(cryptoID).data:
                if (trans.status == "completed"):
                    # if transactions is a sell, the amount was negative
                    self.__walletDict[cryptoID] += float(
                        trans.native_amount.amount)

                    # if is present a sell, add desired earn because in the wallet remain desired earn
                    # check data after change broker logic, in order to not calculate sale before the day when logic change
                    if(not last_sell_found and trans.type == 'sell' and parser.parse(trans.created_at) > datetime.datetime(year=2021, month=10, day=8, tzinfo=pytz.UTC)):
                        self.__walletDict[cryptoID] += self.__DESIRED_EARN
                        last_sell_found = True

    def CryptoSale(self):
        for id, amount in self.__walletDict.items():
            threshold = amount+self.__DESIRED_EARN

            # get current price of crypto
            current_price_crypto = float(
                self.__client.get_account(id).balance.amount)*float(self.__client.get_spot_price(currency_pair=f'{id}-{self.__CURRENCY_EXCHANGE}').amount)

            # check is price is greather than threshold and start sell amount
            if(current_price_crypto > threshold):
                create_sale = self.__client.sell(id, total=str(
                    amount), currency=self.__CURRENCY_EXCHANGE, commit=False)

            # check if total is equal to the amount (check for fee)
                if(float(create_sale.total.amount) == amount):
                    try:
                        self.__client.commit_sell(id, create_sale.id)
                        logger.info(
                            f'Sold {amount} {self.__CURRENCY_EXCHANGE} of {id} crypto')
                    except:
                        logger.warning(
                            f'Failed to commit sell of {amount} {self.__CURRENCY_EXCHANGE} {id} crypto')
