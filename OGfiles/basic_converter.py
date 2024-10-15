# Dictionary representing fiat currencies with their values
fiat = {
    'usd': 1.00,  # US Dollar
    'eur': 0.91,  # Euro
}

# Function to verify and convert currencies
def verify_currency():
    while True:  
        
        fiat_input1 = input('Enter the currency you want to convert: ').lower()
        
        if fiat_input1 in fiat:
            
            fiat_input2 = input(f'Enter the currency you want to convert {fiat_input1.upper()} to: ').lower()

            if fiat_input2 in fiat:
                while True:  
                    print('Currency 2 accepted')
                    amount = float(input(f"Enter the amount to convert from {fiat_input1.upper()} to {fiat_input2.upper()}: "))
                    
                    converted_amount = amount * (fiat[fiat_input2] / fiat[fiat_input1])
                    print(f'{amount} {fiat_input1.upper()} is equivalent to {converted_amount:.2f} {fiat_input2.upper()}.\n')
                    
                    change_currency = input("Do you want to change the currencies? (y for yes, n to continue with the same currencies): ").lower()
                    if change_currency == 'y':
                        break
                    else:
                        continue_conversion = input("Do you want to do another conversion? (y for yes, any other key to exit): ").lower()
                        if continue_conversion != 'y':
                            print("Program terminated.")
                            return
            else:
                fiat_input2 = input(f'{fiat_input2.upper()} is not in our database.\nPlease enter another currency or write -1 to exit: ')
                if fiat_input2 == '-1':
                    print("Program terminated.")
                    break

        else:
            fiat_input1 = input(f'{fiat_input1.upper()} is not in our database.\nPlease enter another currency or write -1 to exit: ')
            if fiat_input1 == '-1':
                print("Program terminated.")
                break


verify_currency()
