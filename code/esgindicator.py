import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def esg_scrape_value(url):
     try:
        response= requests.get(url)
        soup = BeautifulSoup(response.text,'html.parser')

        cssClasses = ['risk-rating-score', 'risk-rating-assessment']
        
        elements = soup.find_all(class_=cssClasses)
        if elements: 
            values = [element.text.strip() for element in elements]
            return values[0] + ", " + values[1]
        else:
            print()
            return ''

     except Exception as e:
        print(f"Error: {e}")
     return None

def esg_get_url(company_name):
    print('inside get url')
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    
    # Set up Chrome WebDriver with headless options
    driver = webdriver.Chrome(options=chrome_options)
    
    url="https://www.sustainalytics.com/esg-ratings"
    
    driver.get(url)
    search_input = driver.find_element("id", "searchInput")  #.find_element_by_id("searchInput")
    search_input.send_keys(company_name) 

    time.sleep(4)
             
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    search_result_list = soup.find('a', {'class':'search-link'})
    if search_result_list:
        return url + search_result_list['data-href']
    else:
        return ''
    
    driver.quit()


