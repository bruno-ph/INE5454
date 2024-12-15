import json

def convert_to_dollar(source_price, source_country):
    currencies_list = open('currencies.json', 'r')
    list = json.load(currencies_list)
    if source_country in list:
        rateToDollar = list[source_country]["rateToDollar"]
        priceInDollar = source_price * rateToDollar
        return priceInDollar
    print("The selected country is not available.")
    return False

if __name__ == "__main__":
    convert_to_dollar(30, "Brazil")