<p align="center"><img src="https://user-images.githubusercontent.com/20209393/138785526-bdf71315-9ba4-4b96-9221-703f1f25df76.png" /></p>

<h2 align="center">Non-official Mercado Bitcoin Trade API Python Wrapper</h2>

`mbpy` is an open source python wrapper to [Mercado Bitcoin Trade API](https://www.mercadobitcoin.com.br/trade-api).

## Features

- Mercado Bitcoin Auth (requires API Key)
- View Account Balance
- Buy & Sell cryptocurrencies
- Manage Orders
- Withdraw/Transfer funds
- View Mercado Bitcoin Public Orderbook info

### Disclaimer

This a non-official script that makes use of a Public API using your user account credentials on Mercado Bitcoin crypto trading platform. It is provided 'as is' without express or implied warranty. Use it at your own risk.

## Setup

### Step 1

Clone the project repository:

```sh
$ git clone github.com/lucianoayres/mbpy.git

```

### Step 2

Make sure you have following Python packages installed:

- hashlib
- hmac
- json
- time
- http
- urlib

### Step 3

mbpy makes use of Mercado Bitcoin´s official Trade API, so log in on their website and [generate your API Key (TAPI ID) and Secret (TAPI SECRET) pair](https://www.mercadobitcoin.com.br/plataforma/chaves-api).

### Step 4

Create a new Python script, import mbpy and create a new instance of it using your TAPI ID and TAPI Secret

```Python
from mbpy import mbpy

mbClient = mbpy('YOUR_TAPI_ID', 'YOUR_TAPI_SECRET')
```

## Usage

```Python
# Place a Market Buy order of R$ 150 in Bitcoin
response = mbClient.placemarketbuyorder('BRLBTC','150')

if response['status_code'] == 100:
  print('success')
else:
  if response['error_message] != '':
    print(response['error_message'])
  else
    print('Mercado Bitcoin API is temporarily unavailable')
```

IMPORTANT: Check [Mercado Bitcoin Trade API](https://www.mercadobitcoin.com.br/trade-api) for a complete list of coin IDs and minimum purchase amount per coin category.

## Examples

```Python
# Place a Buy order of 0.002 Ethereum with a limit price of R$ 700
mbClient.placebuyorder('BRLETH','0.002', '700')
```

```Python
# Place a Market Sell order of 0.005 Bitcoin Cash
mbClient.placemarketsellorder('BRLBCH','0.005')
```

```Python
# Place a Sell order of 0.1 Litecoin with a minimal price of R$ 1.800,50
mbClient.placesellorder('BRLLTC', '0.1', '1800.50')
```

### Additional Methods

Check the source code comments to learn more about the remaining methods:

- listsystemmessages
- getaccountinfo
- getorder
- cancelorder
- listorders
- listorderbook
- withdraw_coin

# Reference

- [Mercado Bitcoin Trade API](https://www.mercadobitcoin.com.br/trade-api)

## License

[MIT License](https://github.com/esqb/brcoin/blob/main/LICENSE)
