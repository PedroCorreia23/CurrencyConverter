import requests

# Function to fetch the real-time price in USD for a given cryptocurrency
def get_price_in_usd(crypto_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd"

    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()  # Parse the JSON response
        return data.get(crypto_id, {}).get('usd', None)
    else:
        print(f"Error: Unable to fetch data (Status code: {response.status_code})")
        print(f"Response Content: {response.text}")  # Debugging information
        return None

# Dictionary representing fiat currencies (as fallback)
fiat = {
    'usd': 1.00,  # US Dollar
    'eur': 0.91,  # Euro
}

# List of supported cryptocurrencies (from CoinGecko)
crypto_supported = ['bitcoin', 'ethereum', 'litecoin']  # Add more as needed

# Map for CoinGecko IDs (to avoid using symbols directly)
coin_gecko_ids = {
    'bitcoin': 'bitcoin',
    'ethereum': 'ethereum',
    'litecoin': 'litecoin'
}

# Function to verify and convert currencies
def verify_currency():
    while True:
        # Get the source currency from user input
        from_currency = input('Enter the currency you want to convert: ').lower()
        
        # Determine if from_currency is fiat or crypto
        if from_currency in fiat:
            from_type = 'fiat'
        elif from_currency in coin_gecko_ids:
            from_type = 'crypto'
        else:
            print(f'{from_currency.upper()} is not in our database. Please enter another currency.')
            continue

        # Get the target currency from user input
        to_currency = input(f'Enter the currency you want to convert {from_currency.upper()} to: ').lower()
        
        # Determine if to_currency is fiat or crypto
        if to_currency in fiat:
            to_type = 'fiat'
        elif to_currency in coin_gecko_ids:
            to_type = 'crypto'
        else:
            print(f'{to_currency.upper()} is not in our database. Please enter another currency.')
            continue

        # For crypto-to-crypto or crypto-to-fiat conversions
        if from_type == 'crypto' and to_type == 'crypto':
            from_currency_id = coin_gecko_ids.get(from_currency)
            to_currency_id = coin_gecko_ids.get(to_currency)

            # Fetch the prices in USD
            from_price_usd = get_price_in_usd(from_currency_id)
            to_price_usd = get_price_in_usd(to_currency_id)

            if from_price_usd is None or to_price_usd is None:
                print(f"Unable to fetch prices for {from_currency.upper()} or {to_currency.upper()}")
                continue

            # Calculate the conversion rate (from_crypto in to_crypto)
            rate = from_price_usd / to_price_usd
            print(f"1 {from_currency.upper()} is equivalent to {rate:.6f} {to_currency.upper()}")

        # Perform fiat-to-fiat or fiat-to-crypto conversions
        elif from_type == 'fiat' or to_type == 'fiat':
            if from_type == 'fiat' and to_type == 'fiat':
                # Use the fallback fiat rates
                rate = fiat[to_currency] / fiat[from_currency]
            else:
                # Crypto-to-fiat or fiat-to-crypto
                crypto_id = coin_gecko_ids.get(from_currency, from_currency) if from_type == 'crypto' else coin_gecko_ids.get(to_currency, to_currency)
                price_in_usd = get_price_in_usd(crypto_id)
                if price_in_usd is None:
                    print(f"Unable to fetch price for {from_currency.upper()} or {to_currency.upper()}")
                    continue
                rate = price_in_usd if from_type == 'crypto' else 1 / price_in_usd

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


verify_currency()
