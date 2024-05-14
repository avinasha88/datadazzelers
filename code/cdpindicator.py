import requests
from bs4 import BeautifulSoup
def scrape_value(url, cssClasses):
    try:
        response= requests.get(url)
        soup = BeautifulSoup(response.text,'html.parser')
        
        elements = soup.find_all(class_=cssClasses)
        if elements: 
            values = [element.text.strip() for element in elements]
            return values
        else:
            print()
            return None

    except Exception as e:
        print(f"Error: {e}")
    return None

def get_url(company_name):
    return "https://www.cdp.net/en/responses?queries%5Bname%5D="+company_name