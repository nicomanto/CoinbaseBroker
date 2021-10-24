from Broker import Broker
import time
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def main():
    broker = Broker()

    logger.info("Start to negotiate")
    while(True):
        broker.CryptoSale()
        broker.UpdateWallet()
        time.sleep(2.5)


if __name__ == "__main__":
    main()
