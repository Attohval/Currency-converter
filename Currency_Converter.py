import requests
import time

api_key = "" #API_KEY 

url = f"https://v6.exchangerate-api.com/v6/{api_key}/codes"# Fetch the list of supported currencies
try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    if 'supported_codes' in data:
        supported_currencies = [code for code, name in data['supported_codes']]
    else:
        print("Invalid response from API.")
        supported_currencies = None
except requests.exceptions.HTTPError:
    print("Check API key or URL.")
    supported_currencies = None
except Exception:
    print("Check API key or URL.")
    supported_currencies = None

if not supported_currencies:
    print("Could not fetch supported currencies.")
else:
    while True:
        from_currency = input("Enter the currency to change from (e.g., USD, NGN, EUR): ").strip().upper()
        to_currency = input("Enter the currency to change to (e.g., USD, NGN, EUR): ").strip().upper()

        if from_currency not in supported_currencies:
            print(f"Invalid currency: {from_currency}")
            continue
        if to_currency not in supported_currencies:
            print(f"Invalid currency: {to_currency}")
            continue
        
        amount = float(input("Enter the amount to convert: "))

        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{from_currency}"  # Fetch the exchange rate
        
        retries = 2
        delay = 2
        for attempt in range(retries):
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an HTTPError for bad responses
                data = response.json()
                
                if 'conversion_rates' in data:
                    conversion_rate = data['conversion_rates'].get(to_currency)
                    
                    if conversion_rate is not None:
                        converted_amount = amount * conversion_rate
                        print("")
                        print(f"Exchange rate from {from_currency} to {to_currency}: {conversion_rate}")
                        print(f"{amount} {from_currency} is equivalent to {converted_amount:.2f} {to_currency}")
                        break
                    else:
                        print(f"Error: Conversion rate for {to_currency} not found.")
                        break
                else:
                    print("Error: Invalid response from API.")
                    break

            except requests.exceptions.HTTPError:
                print("HTTP error occurred while fetching exchange rate.")
                if attempt < retries - 1:
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    print("HTTP error. Unable to fetch exchange rate.")
                    break
            except Exception as err:
                print("Error occurred while fetching exchange rate.")
                if attempt < retries - 1:
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    print("Error. Unable to fetch exchange rate.")
                    break
        else:
            continue
        break