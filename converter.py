import requests

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

# Function to fetch the real-time price in USD for a given cryptocurrency
def get_price_in_usd(crypto_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data.get(crypto_id, {}).get('usd', None)
    else:
        print(f"Error: Unable to fetch data (Status code: {response.status_code})")
        return None

# Function to verify and convert currencies
def verify_currency():
    # Show ticker symbol usage alert
    print("Please use the **ticker symbols** (e.g., 'btc' for Bitcoin, 'eth' for Ethereum, 'sol' for Solana).")
    
    # Fetch supported coins from CoinGecko
    coin_mapping = get_supported_coins()
    
    if not coin_mapping:
        print("Error fetching coin data from CoinGecko.")
        return

    print(f"Successfully loaded {len(coin_mapping)} supported coins.")

    while True:
        # Get the source currency from user input
        from_currency = input('Enter the currency you want to convert (ticker symbol): ').lower()

        if from_currency not in coin_mapping:
            print(f"Invalid currency! Please enter the **ticker symbol** (e.g., 'btc', 'eth', 'sol'). '{from_currency.upper()}' is not in our list.")
            continue

        # Get the target currency from user input
        to_currency = input(f'Enter the currency you want to convert {from_currency.upper()} to (ticker symbol): ').lower()

        if to_currency not in coin_mapping:
            print(f"Invalid currency! Please enter the **ticker symbol** (e.g., 'btc', 'eth', 'sol'). '{to_currency.upper()}' is not in our list.")
            continue

        from_currency_id = coin_mapping[from_currency]
        to_currency_id = coin_mapping[to_currency]

        # Fetch the prices in USD for both cryptocurrencies
        from_price_usd = get_price_in_usd(from_currency_id)
        to_price_usd = get_price_in_usd(to_currency_id)

        # Print fetched USD prices for debugging
        print(f"Price of 1 {from_currency.upper()} in USD: {from_price_usd}")
        print(f"Price of 1 {to_currency.upper()} in USD: {to_price_usd}")

        if from_price_usd is None or to_price_usd is None:
            print(f"Unable to fetch prices for {from_currency.upper()} or {to_currency.upper()}")
            continue

        # Calculate the conversion rate correctly
        rate = from_price_usd / to_price_usd
        print(f"1 {from_currency.upper()} is equivalent to {rate:.6f} {to_currency.upper()}")

        # Perform the conversion
        amount = float(input(f"Enter the amount to convert from {from_currency.upper()} to {to_currency.upper()}: "))
        converted_amount = amount * rate
        print(f'{amount} {from_currency.upper()} is equivalent to {converted_amount:.6f} {to_currency.upper()}.\n')

        # Ask if the user wants to change currencies or do another conversion
        change_currency = input("Do you want to change the currencies? (y for yes, n to continue with the same currencies): ").lower()
        if change_currency == 'y':
            continue
        else:
            continue_conversion = input("Do you want to do another conversion? (y for yes, any other key to exit): ").lower()
            if continue_conversion != 'y':
                print("Program terminated.")
                return

# Run the converter
verify_currency()
