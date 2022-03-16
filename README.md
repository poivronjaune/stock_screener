# TSX Stock Screener and Indicators

Work in progress (just fooling around with TSX Stocks data), no documentation for the moment.  
Requires a local SQLite3 database with stock prices for TSX exchange.  
Historical data by year for many TSX symbols provided in CSV files  

Warning:  
Bad code implementation, so no comments on code quality please.  

#### Solution components  
![Solution](/images/ComponentsArchitecture.PNG)

## Building the local database  
- Download the zip files from github
- Unzip all prices as CSV in the main folder of the project
- Open the ``DataQualityAnalysis.ipynb`` notebook  
- Goto the CREATE DB FROM CSV Files  
- Change the db_name variable to the name of the SQLITE file you want ot use
- Remove comments from the symbols or prices_daily commands  
- Run the cell  
A global variable ``database_name`` is used for all function expect the create DB functions. Make sur to update the global name after creating your local copy



# prices_daily
- Date    : text
- Ticker  : text
- Open    : real
- High    : real
- Low     : real
- Close   : real
- Volume  : real

# Symbols
- ticker  : text
- name    : text
- exchange: text

## Selenium requirements
https://chromedriver.chromium.org/downloads
