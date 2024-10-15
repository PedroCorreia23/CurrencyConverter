import requests

# Define your ExchangeRate-API key
FIAT_API_KEY = 'cd10a4a0d36f903b73894034'  # Replace with your real API key from ExchangeRate-API

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
    # Simple check for common cryptocurrencies, can add more as needed
    crypto_symbols = ['btc', 'eth', 'sol', 'ltc', 'xrp']  # Add more symbols if needed
    return currency in crypto_symbols

# Function to verify and convert currencies
def verify_currency():
    # Show ticker symbol usage alert
    print("Please use **ticker symbols** (e.g., 'btc' for Bitcoin, 'eth' for Ethereum) or ISO codes for fiat (e.g., 'usd', 'eur').")
    
    # Fetch supported coins from CoinGecko
    coin_mapping = get_supported_coins()
    
    if not coin_mapping:
        print("Error fetching coin data from CoinGecko.")
        return

    print(f"Successfully loaded {len(coin_mapping)} supported coins.")

    while True:
        # Get the source currency from user input
        from_currency = input('Enter the currency you want to convert (ticker symbol or fiat code): ').lower()

        # Check if the source currency is crypto or fiat
        if from_currency in coin_mapping:
            from_currency_type = 'crypto'
        else:
            from_currency_type = 'fiat'
        
        # Get the target currency from user input
        to_currency = input(f'Enter the currency you want to convert {from_currency.upper()} to (ticker symbol or fiat code): ').lower()

        # Check if the target currency is crypto or fiat
        if to_currency in coin_mapping:
            to_currency_type = 'crypto'
        else:
            to_currency_type = 'fiat'

        # Handle crypto-to-crypto conversion
        if from_currency_type == 'crypto' and to_currency_type == 'crypto':
            from_currency_id = coin_mapping[from_currency]
            to_currency_id = coin_mapping[to_currency]

            # Fetch the prices in USD for both cryptocurrencies
            from_price_usd = get_price_in_usd(from_currency_id)
            to_price_usd = get_price_in_usd(to_currency_id)

            if from_price_usd is None or to_price_usd is None:
                print(f"Unable to fetch prices for {from_currency.upper()} or {to_currency.upper()}")
                continue

            # Calculate the conversion rate
            rate = from_price_usd / to_price_usd
            print(f"1 {from_currency.upper()} is equivalent to {rate:.6f} {to_currency.upper()}")

            # Perform the conversion
            amount = float(input(f"Enter the amount to convert from {from_currency.upper()} to {to_currency.upper()}: "))
            converted_amount = amount * rate
            print(f'{amount} {from_currency.upper()} is equivalent to {converted_amount:.6f} {to_currency.upper()}.\n')

        # Handle fiat-to-fiat conversion
        elif from_currency_type == 'fiat' and to_currency_type == 'fiat':
            rate, converted_amount = get_fiat_rate(from_currency, to_currency)

            if rate is None:
                print(f"Unable to fetch exchange rate for {from_currency.upper()} to {to_currency.upper()}")
                continue

            amount = float(input(f"Enter the amount to convert from {from_currency.upper()} to {to_currency.upper()}: "))
            print(f"Exchange rate: {rate:.6f}")
            print(f"{amount} {from_currency.upper()} is equivalent to {amount * rate:.2f} {to_currency.upper()}.\n")

        # Handle crypto-to-fiat conversion
        elif from_currency_type == 'crypto' and to_currency_type == 'fiat':
            from_currency_id = coin_mapping[from_currency]
            from_price_usd = get_price_in_usd(from_currency_id)
            rate, _ = get_fiat_rate('usd', to_currency)

            if from_price_usd is None or rate is None:
                print(f"Unable to fetch prices for {from_currency.upper()} or {to_currency.upper()}")
                continue

            amount = float(input(f"Enter the amount to convert from {from_currency.upper()} to {to_currency.upper()}: "))
            converted_amount = amount * from_price_usd * rate
            print(f"{amount} {from_currency.upper()} is equivalent to {converted_amount:.2f} {to_currency.upper()}.\n")

        # Handle fiat-to-crypto conversion
        elif from_currency_type == 'fiat' and to_currency_type == 'crypto':
            to_currency_id = coin_mapping[to_currency]
            to_price_usd = get_price_in_usd(to_currency_id)
            rate, _ = get_fiat_rate(from_currency, 'usd')

            if to_price_usd is None or rate is None:
                print(f"Unable to fetch prices for {from_currency.upper()} or {to_currency.upper()}")
                continue

            amount = float(input(f"Enter the amount to convert from {from_currency.upper()} to {to_currency.upper()}: "))
            converted_amount = (amount / rate) / to_price_usd
            print(f"{amount} {from_currency.upper()} is equivalent to {converted_amount:.6f} {to_currency.upper()}.\n")

        else:
            print("Invalid input. Please try again.")

        # Ask if the user wants to perform another conversion
        change_currency = input("Do you want to perform another conversion? (y for yes, any other key to exit): ").lower()
        if change_currency != 'y':
            print("Program terminated.")
            break

# Run the converter
verify_currency()
