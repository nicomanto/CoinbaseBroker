from src.Broker import Broker
import time


def main():
    broker = Broker()

    while(True):
        broker.CryptoSale()
        broker.UpdateWallet()
        time.sleep(2.5)


if __name__ == "__main__":
    main()
