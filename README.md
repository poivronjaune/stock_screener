# TSX Stock Screener and Indicators

Work in progress (just fooling around with TSX Stocks data), no documentation for the moment.  
Requires a local SQLite3 database with stock prices for TSX exchange.  
Historical data by year for many TSX symbols provided in CSV files  

Warning:  
Bad code implementation, so no comments on code quality please.  

#### Solution components  
![Solution](/images/ComponentsArchitecture.PNG)

## Building the local database  

For those who want to rebuild the prices database. Try to use the first 2 cells of the jupyter notebook. Use at your own risk.

#### prices_daily
- Date    : text
- Ticker  : text
- Open    : real
- High    : real
- Low     : real
- Close   : real
- Volume  : real

#### Symbols
- ticker  : text
- name    : text
- exchange: text

