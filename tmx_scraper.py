import time
import warnings

import pandas as pd

from datetime import datetime
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TMXScraper:
    def __init__(self) -> None:
        self.driver = None
        self.wait = None

        self.open_browser() # Creates driver and wait objects for selenium

    def scrap_pages(self, ticker, pages=1):
        """ Main scraper to extract table price data from TMX Web site """
        if self.open_page(ticker):
            data = self.scrap_data_from_page()
            result = pd.DataFrame(data=data)
        else:
            result = None
        
        return result

    def close(self):
        self.driver.quit()
        del self
    
    # UTILITY FUNCTIONS FOR CLASS
    def open_browser(self):
        """ Create a selenium driver object name self.driver. Create a default WebDriverWait object """
        # Setup Selenium browser
        CHROME_DRIVER_LOCATION = "chromedriver.exe"
        service_object = Service(CHROME_DRIVER_LOCATION)

        OPTIONS = webdriver.ChromeOptions()
        OPTIONS.add_argument('--ignore-certicate-errors')
        OPTIONS.add_argument('--incognito')
        #OPTIONS.add_argument('--headless')
        OPTIONS.add_experimental_option('excludeSwitches', ['enable-logging'])
       
        #self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER_LOCATION,options=OPTIONS)
        self.driver = webdriver.Chrome(service=service_object, options=OPTIONS)
        WebDriverWait(self.driver, 10)    
        warnings.filterwarnings("ignore", category=DeprecationWarning)     

    def open_page(self, symbol):
        """ Open the URL page for TMX symbol. Create driver if None """
        if self.driver is None:
            self.open_browser()

        tmx_url = f"https://money.tmx.com/en/quote/{symbol}/trade-history?selectedTab=price-history"
        try:
            self.driver.get(tmx_url)
            time.sleep(5)
            ad_closed = self.close_add()
            return True
        except Exception as e:
            print(f"Could not open ticker page : {e}")
            return False

    def scrap_data_from_page(self):
        ad_closed = self.close_add()
        if ad_closed:
            data = self.extract_html_table()

        return data


    def close_add(self):
        """ Close the op level add that is on the TMX trade history page to expose the next_button """
        try:
            close_ad_btn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'ssrt-close-anchor-button')))
        except Exception as e:
            print(f"Unable to close_ads : {e}")  
            return False 

        try:
            close_ad_btn.click()
        except:
            # TODO: Fix this required try clause (bad practice)     
            pass
        return True

    def extract_html_table(self):
        """ Extract the price data from HTML using Pandad read_html method """
        d = datetime.today().strftime('%Y-%m-%d')
        empty_data = {
            "Date"        : [d],
            "Open ($)"    : "0.00",
            "High ($)"    : "0.00",
            "Low ($)"     : "0.00",
            "Close ($)"   : "0.00",
            "VWAP ($)"    : "0.00",
            "Change ($)"  : "0.00",
            "Change (%)"  : "0.00",
            "Volume"      : "0",
            "Trade Value" : "0.00",
            "# Trades" : "0.00",
        }

        html_page = self.driver.page_source        
        try:
            data = pd.read_html(html_page)
            prices_df = data[0]
        except:
            prices_df = pd.DataFrame(data=empty_data)

        prices_df['Date'] = pd.to_datetime(prices_df["Date"], infer_datetime_format=True)

        return prices_df



if __name__ == "__main__":
    print("Testing tmx_scraper functions")
    scraper = TMXScraper()
    result = scraper.scrap_one_page("ABCT")
    print(result)
    scraper.close()
