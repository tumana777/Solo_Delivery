import requests, datetime

def get_exchange_rate(currency_code):
    today = datetime.date.today()
    formatted_date = today.strftime('%Y-%m-%d')
    url = f"https://nbg.gov.ge/gw/api/ct/monetarypolicy/currencies/?date={formatted_date}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        for item in data[0]['currencies']:
            if item['code'] == currency_code:
                return item['rate'] / item['quantity']
        raise ValueError(f"Currency {currency_code} not found")
    else:
        raise Exception("Failed to fetch exchange rates")