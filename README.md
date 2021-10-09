# CoinbaseBroker

Coinbase broker that sells cryptocurrencies after specific thresholds

## Thresholds

The formula is:

```
if(current_price > buy_price+DESIRED_EARN+fee) -> sell buy_price
```

So remains **DESIRED_EARN** in the wallet after sell

## Usage

Replace the **API_KEY** and **API_SECRET** with the API created by Coinbase. Change the current `CURRENCY_EXCHANGE` and `DESIRED_EARN` if needed. Next run `python src/main.py`
