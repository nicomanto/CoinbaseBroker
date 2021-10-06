
from coinbase.wallet.client import Client
import logging
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# set API KEY created on Coinbase
API_KEY = os.environ.get('API_KEY', None)
API_SECRET = os.environ.get('API_SECRET', None)


class Broker:

    def __init__(self):
        logger.info("Create broker")
        self.__client = Client(API_KEY, API_SECRET)
        # set threshold param
        self.__CURRENCY_EXCHANGE = 'EUR'
        self.__FACTOR_EXCHANGE = 2
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

                    # add last sell to amount because broker sell AMOUNT after it exceeds the AMOUNT*2, so AMOUNT remains in the wallet
                    if(not last_sell_found and trans.type == 'sell'):
                        self.__walletDict[cryptoID] += -float(
                            trans.native_amount.amount)
                        last_sell_found = True

    def CryptoSale(self):
        for id, amount in self.__walletDict.items():
            print(id, amount)
            threshold = amount*self.__FACTOR_EXCHANGE

            # get current price of crypto
            current_price_crypto = float(
                self.__client.get_account(id).balance.amount)*float(self.__client.get_spot_price(currency_pair=f'{id}-{self.__CURRENCY_EXCHANGE}').amount)

            # check is price is greather than threshold
            if(current_price_crypto > threshold):
                create_sale = self.__client.sell(id, total=str(
                    amount), currency=self.__CURRENCY_EXCHANGE, commit=False)

            # check if total is equal to the threshold (check for fee)
                if(float(create_sale.total.amount) == amount):
                    try:
                        self.__client.commit_sell(id, create_sale.id)
                        logger.info(
                            f'Sold {threshold} {self.__CURRENCY_EXCHANGE} of {id} crypto')
                    except:
                        logger.warning(
                            f'Failed to commit sell of {threshold} {self.__CURRENCY_EXCHANGE} {id} crypto')
