import requests
from bs4 import BeautifulSoup

def fetch_us_10y_yield():
    url = "https://fred.stlouisfed.org/series/DGS10"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    yield_element = soup.find('span', class_='series-meta-observation-value')
    if yield_element:
        yield_value = yield_element.text.strip().replace('%', '')
        return float(yield_value)
    return None

def graham_valuation(data):
    try:
        eps = data["eps"]
        growth = data["growth"] * 100
        discount_rate = fetch_us_10y_yield()
        if discount_rate is None:
            return None
        return round((eps * (7 + 1 * growth)) * 4.4 / discount_rate, 2)
    except:
        return None
