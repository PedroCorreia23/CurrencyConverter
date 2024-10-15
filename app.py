from flask import Flask, render_template, request
import requests

app = Flask(__name__)

FIAT_API_KEY = 'cd10a4a0d36f903b73894034'  # Add your real API key here

# Function to fetch fiat conversion rate using ExchangeRate-API
def get_fiat_rate(from_currency, to_currency, amount=None):
    if amount:
        url = f"https://v6.exchangerate-api.com/v6/{FIAT_API_KEY}/pair/{from_currency.upper()}/{to_currency.upper()}/{amount}"
    else:
        url = f"https://v6.exchangerate-api.com/v6/{FIAT_API_KEY}/pair/{from_currency.upper()}/{to_currency.upper()}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data.get('conversion_rate'), data.get('conversion_result', None)
    else:
        print(f"Error: Unable to fetch fiat currency data (Status code: {response.status_code})")
        return None, None

# Function to fetch all supported coins from CoinGecko
def get_supported_coins():
    url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(url)

    if response.status_code == 200:
        coins_list = response.json()
        # Map symbols to their corresponding CoinGecko IDs
        coin_mapping = {coin['symbol']: coin['id'] for coin in coins_list}
        return coin_mapping
    else:
        print(f"Error: Unable to fetch supported coins (Status code: {response.status_code})")
        return {}

# Function to fetch the real-time price in USD for a given cryptocurrency (CoinGecko)
def get_price_in_usd(crypto_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data.get(crypto_id, {}).get('usd', None)
    else:
        print(f"Error: Unable to fetch cryptocurrency data (Status code: {response.status_code})")
        return None

# Function to check if the input is a cryptocurrency
def is_crypto(currency):
    # Simple check for common cryptocurrencies
    crypto_symbols = ['btc', 'eth', 'sol', 'ltc', 'xrp'] 
    return currency in crypto_symbols

@app.route('/')
def index():
    return render_template('index.html')

from flask import request

@app.route('/convert', methods=['POST'])
def convert():
    try:
        # Fetch JSON data from the request body
        data = request.get_json()
        from_currency = data['from_currency'].lower()
        to_currency = data['to_currency'].lower()
        amount = float(data['amount'])  # Ensure amount is a float

        # Print form data to check
        print(f"From Currency: {from_currency}")
        print(f"To Currency: {to_currency}")
        print(f"Amount: {amount}")
        
        coin_mapping = get_supported_coins()
        
        if from_currency in coin_mapping:
            from_currency_type = 'crypto'
        else:
            from_currency_type = 'fiat'
        
        if to_currency in coin_mapping:
            to_currency_type = 'crypto'
        else:
            to_currency_type = 'fiat'
        
        # Crypto-to-crypto conversion
        if from_currency_type == 'crypto' and to_currency_type == 'crypto':
            from_currency_id = coin_mapping[from_currency]
            to_currency_id = coin_mapping[to_currency]

            from_price_usd = get_price_in_usd(from_currency_id)
            to_price_usd = get_price_in_usd(to_currency_id)

            if from_price_usd is None or to_price_usd is None:
                return f"Unable to fetch prices for {from_currency.upper()} or {to_currency.upper()}.", 400

            rate = from_price_usd / to_price_usd
            converted_amount = amount * rate  # amount is already a float
            return f"{amount} {from_currency.upper()} is equivalent to {converted_amount:.6f} {to_currency.upper()}."

        # Fiat-to-fiat conversion
        elif from_currency_type == 'fiat' and to_currency_type == 'fiat':
            rate, _ = get_fiat_rate(from_currency, to_currency)

            if rate is None:
                return f"Unable to fetch exchange rate for {from_currency.upper()} to {to_currency.upper()}.", 400

            converted_amount = amount * rate  # amount is already a float
            return f"{amount} {from_currency.upper()} is equivalent to {converted_amount:.2f} {to_currency.upper()}."

        # Crypto-to-fiat conversion
        elif from_currency_type == 'crypto' and to_currency_type == 'fiat':
            from_currency_id = coin_mapping[from_currency]
            from_price_usd = get_price_in_usd(from_currency_id)
            rate, _ = get_fiat_rate('usd', to_currency)

            if from_price_usd is None or rate is None:
                return f"Unable to fetch prices for {from_currency.upper()} or {to_currency.upper()}.", 400

            converted_amount = amount * from_price_usd * rate  # amount is already a float
            return f"{amount} {from_currency.upper()} is equivalent to {converted_amount:.2f} {to_currency.upper()}."

        # Fiat-to-crypto conversion
        elif from_currency_type == 'fiat' and to_currency_type == 'crypto':
            to_currency_id = coin_mapping[to_currency]
            to_price_usd = get_price_in_usd(to_currency_id)
            rate, _ = get_fiat_rate(from_currency, 'usd')

            if to_price_usd is None or rate is None:
                return f"Unable to fetch prices for {from_currency.upper()} or {to_currency.upper()}.", 400

            converted_amount = (amount / rate) / to_price_usd  # amount is already a float
            return f"{amount} {from_currency.upper()} is equivalent to {converted_amount:.6f} {to_currency.upper()}."
        
        return "Invalid input.", 400

    except KeyError as e:
        return f"Missing required field: {str(e)}", 400
    
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


if __name__ == '__main__':
    app.run(debug=True)

