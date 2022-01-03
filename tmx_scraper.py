import os
import time
import warnings
import random
from numpy import result_type

import pandas as pd

from datetime import datetime
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def multi_browser_scrap(tickers, browser_qty):
    drivers = []
    data = []

    # Open Browsers
    for id in range(0,browser_qty):
        drivers.append(TMXScraper(ID=id))
        data.append(None)
    
    # Loop through tickers
    ticker_index = 0
    while ticker_index < len(tickers):        
        for id in range(0,browser_qty):
            ticker_offset = ticker_index + id
            if ticker_offset < len(tickers):
                drivers[id].open_page(tickers[ticker_offset])
                data[id] = drivers[id].scrap_data_from_page()
                data[id].to_csv(f"CSV\{tickers[ticker_offset]}.csv", mode='w', header=True)
        
        ticker_index = ticker_index + browser_qty

class TMXScraper:
    def __init__(self, ID=1, headless=False) -> None:
        self.driver = None
        self.wait = None
        self.id = ID

        self.open_browser() # Creates driver and wait objects for selenium

    def scrap_pages(self, ticker, pages=1):
        """ Main scraper to extract table price data from TMX Web site """
        if self.open_page(ticker):
            data = self.scrap_data_from_page()
            result = pd.DataFrame(data=data)
        else:
            result = None
        
        return result

    def scrap_symbols(self, letter, exchange):
        if self.open_symbols_page(letter,exchange):
            data = self.scrap_symbols_from_page()
            result = pd.DataFrame(data=data)
            result['exchange'] = exchange
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
        self.full_path = os.path.abspath(".\ChromeProfile")
        service_object = Service(CHROME_DRIVER_LOCATION)

        OPTIONS = webdriver.ChromeOptions()
        OPTIONS.add_argument('--ignore-certicate-errors')
        OPTIONS.add_argument('--incognito')
        #OPTIONS.add_argument('--headless')
        OPTIONS.add_argument(f'--user-data-dir={self.full_path}\Profile{self.id}')
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
            # random_delay = random.randint(3, 9)
            # print(f"Random sleep delay : {random_delay}")
            # time.sleep(random_delay)
            ad_closed = self.close_add()
            return True
        except Exception as e:
            print(f"Could not open ticker page : {e}")
            return False
    
    def open_symbols_page(self, letter, exchange):
        """ Open the URL page for TMX symbols listed. Create driver if None """
        if self.driver is None:
            self.open_browser()

        tsx_url = f"https://www.tsx.com/listings/listing-with-us/listed-company-directory"
        # Set exchange for page
        try:
            self.driver.get(tsx_url)
            btn_switch = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'exchange-toggle')))
            if exchange == "tsx" and btn_switch.get_attribute("class") == "btn-switch invert":
                btn_switch.click()
            if exchange == "tsxv" and btn_switch.get_attribute("class") == "btn-switch":
                btn_switch.click()
        except Exception as e:
            print(f"Unable to locate exchange-toggle button, ",e)
            return False

        # Push letter+ENTER in search field
        try:
            search = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'query')))
            search.send_keys(letter + Keys.ENTER)
        except Exception as e:
            print(f"Unable to send_keys in inut field [{letter} ], ",e)
            return False

        return True

    def scrap_data_from_page(self):
        ad_closed = self.close_add()
        if ad_closed:
            data = self.extract_html_table()

        return data

    def scrap_symbols_from_page(self):
        # Extract data using selenium ad create a list
        try:
            #WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[text()='Symbol']")))
            result_data_xpath = '//*[@id="tresults"]/tbody'
            WebDriverWait(self.driver, 5).until( EC.visibility_of_element_located((By.XPATH, result_data_xpath)))
            datagrid = self.driver.find_element_by_xpath(result_data_xpath)
        except Exception as e:
            print(f"Unable to locate HTML Table containing listing data, ",e)
            return {}   

        data = self.extract_symbols_from_html_table(datagrid)
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

    def extract_symbols_from_html_table(self, datagrid):
        """ Extract symbols and company info from HTML table. Pandas read_HTML does not work on this page """
        data_rows = datagrid.find_elements(By.TAG_NAME, "tr")
        data = []
        for row in data_rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            # Skip the line with no ticker symbol
            if (cells[1].text != ""):
                ticker = cells[1].text
                name = cells[0].text
                url = f"https://money.tmx.com/en/quote/{ticker}"
                row_info = {"ticker": ticker, "company":name.strip(), "url":url, "yahoo":"-"}
                data.append(row_info)

        return data



if __name__ == "__main__":
    print("Testing tmx_scraper functions")
    #scraper = TMXScraper()
    #result = scraper.scrap_one_page("ABCT")
    #result = scraper.scrap_symbols("A", "tsxv")
    #print(result)
    #scraper.close()


    multi_browser_scrap(["ABCT", "ABR", "LWRK", "HDGE", "DRX", "ACO.Y", "HSH"], 3)

