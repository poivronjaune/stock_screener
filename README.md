# TSX Stock Screener

Work in progress (just fooling around with TSX Stocks data), no documentation for the moment.  
Requires a local SQLite3 database with stock prices for TSX exchange.  
Available historical data by year for some TSX symbols  

Warning:  
Bad code implementation, so no comments on code quality please.  


### SQL Lite 3 data base schema  
For those who want to rebuild the prices database. Try to use the first 2 cells of the jupyter notebook. Use at your own risk.

#### prices_daily
- index   : integer
- Date    : text
- Ticker  : text
- Open    : real
- High    : real
- Low     : real
- Close   : real
- Volume  : real

#### Symbols
- index   : integer
- ticker  : text
- name    : text
- exchange: text
- url     : text
- yahoo   : text
