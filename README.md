# CoinbaseBroker

Coinbase broker that sells cryptocurrencies after specific thresholds

## Thresholds

The Broker sell crypto if current price is at least the _double amount of buy price_.

The formula is:

```
if(current_price > buy_price*2) -> sell buy_price
```

So remains **buy_price** in the wallet after sell

## Usage

Replace the **API_KEY** and **API_SECRET** with the API created by Coinbase. Change the current `CURRENCY_EXCHANGE` and `FACTOR_EXCHANGE` if needed. Next run `python src/main.py`
