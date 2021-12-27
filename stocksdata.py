import os.path
import time
import pandas as pd
import sqlite3

from datetime import date, datetime
from dataclasses import dataclass, field

@dataclass
class StocksData:
    db: str

    drive        : str = field(init=False)
    path         : str = field(init=False)
    filename     : str = field(init=False)
    full_path    : str = field(init=False)
    db_size      : int = field(init=False)
    last_update  : time = field(init=False)
    db_type      : str = field(init=False)
    
    # Count are information for symbols tabele
    count_symbols: int = field(init=False)
    count_tsx    : int = field(init=False)
    count_tsxv   : int = field(init=False)

    # Stats are mesures for prices_daily table
    stats_prices    : int = field(init=False)           # All prices rows present in prices_daily table
    stats_tickers   : int = field(init=False)           # Unique tickers present in prices_daily table
    stats_missing   : int = field(init=False)           # Missing tickers in prices_daily vs tickers in symbols


    def __post_init__(self):
        if os.path.exists(self.db):
            self.full_path = os.path.abspath(self.db)
            drivepath, self.filename = os.path.split(self.full_path)
            self.drive, self.path = os.path.splitdrive(drivepath)
            self.last_update = os.path.getmtime(self.db)
            self.db_size = os.path.getsize(self.db)
            self.last_update = datetime.fromtimestamp(os.path.getmtime(self.db)).strftime("%Y-%m-%d %H:%M:%S")
            self.set_db_type()
            self.update_symbols_stats()
            self.update_prices_stats()
            
        else:
            self.db = None
            raise NameError(f"File does not exist : {self.db} ")

    def set_db_type(self):
        """ Detect and set the database type, currently only supprts SQLite 3 databases """
        if (self.db != ""):
            try:
                with open(self.db, 'rb') as fd: header = fd.read(100)
                fd.close()
            except:
                self.db_type = "Unknown"
                return False

            if (header[:16] == b'SQLite format 3\x00'):
                self.db_type = "SQLite3"
                return True
            else:
                self.db_type = "Unknown"
                return False

    def connect(self):
        """ Connect to the database and return the connection engine """
        try:
            con1 = sqlite3.connect(self.db)
            return con1
        except Exception as e:
            return None

    def update_symbols_stats(self):
        """ Update symbols table statistics using SQL commands """
        conn = self.connect()
        if conn is not None:
            cur = conn.cursor()
            cur.execute("SELECT count(*) FROM 'symbols'")
            self.count_symbols = cur.fetchone()[0]
            cur.execute("SELECT count(*) FROM 'symbols' as s WHERE s.exchange == 'tsx'")
            self.count_tsx = cur.fetchone()[0]
            cur.execute("SELECT count(*) FROM 'symbols' as s WHERE s.exchange == 'tsxv'")
            self.count_tsxv = cur.fetchone()[0]
            
            cur.close()
            conn.close()
        else:
            self.count_symbols = None
            self.count_tsx     = None
            self.count_tsxv    = None

    def update_prices_stats(self):
        """ Update prices table statistics using SQL commands"""
        conn = self.connect()
        if conn is not None:
            cur = conn.cursor()
            cur.execute("SELECT count(*) FROM 'prices_daily'")
            self.stats_prices = cur.fetchone()[0]
            cur.execute("SELECT COUNT (DISTINCT Ticker) FROM 'prices_daily'")
            self.stats_tickers = cur.fetchone()[0]
            self.stats_missing = self.count_symbols - self.stats_tickers
            cur.close()
            conn.close()

    def count_prices_per_ticker(self, count=True):
        """ Count number of price rows per ticker symbol. If count=False, skip count and return the DISTINCT ticker list without counting"""
        conn = self.connect()
        if count:
            sql3 = "SELECT DISTINCT prices_daily.Ticker, symbols.name, min(prices_daily.Date) as start_date, max(prices_daily.Date) as end_date, count(prices_daily.Ticker) as price_rows FROM prices_daily INNER JOIN symbols ON prices_daily.Ticker = symbols.ticker GROUP BY prices_daily.ticker ORDER BY prices_daily.ticker"
            prices_data1 = pd.read_sql_query(sql3, conn)
            prices_data1['Ticker'] = prices_data1['Ticker']
            prices_data1['name'] = prices_data1['name']
            prices_data1['start_date'] = pd.to_datetime(prices_data1['start_date']).dt.date
            prices_data1['end_date'] = pd.to_datetime(prices_data1['end_date']).dt.date
            prices_data1['price_rows'] = prices_data1['price_rows'].astype('int32')
        else:
            d = datetime.today().strftime('%Y-%m-%d')
            empty_data = {
                "Ticker": ["None"],
                "Company Name": ["None"],
                "Start Date" : [d],
                "End Date" : [d],
                "Price Rows" : 0
            }
            prices_data1 = pd.DataFrame(empty_data)
        
        conn.close()
        return prices_data1        

    def update_prices_daily(self, ticker, price_data):
        conn = self.connect()
        if conn is not None:
            symbol_to_load = ticker
            existing_prices_df = pd.read_sql(f"SELECT * FROM 'prices_daily' WHERE Ticker='{symbol_to_load}' ORDER BY Date DESC LIMIT 1", conn)

        try:
            last_date = existing_prices_df.loc[0]["Date"]
            new_prices_df = price_data.loc[price_data["Date"] > last_date]
        except KeyError:
            last_date = None
            new_prices_df = price_data

        # Structure the data according to database table structure
        new_prices_df.drop(['VWAP ($)', 'Change ($)', 'Trade Value', '# Trades', 'Change (%)'], axis=1, inplace=True)
        new_prices_df.rename(columns={'Open ($)': 'Open', 'High ($)': 'High', 'Low ($)': 'Low', 'Close ($)': 'Close'  }, inplace=True)
        new_prices_df["Ticker"] = symbol_to_load
        #new_prices_df['Date'] = pd.to_datetime(data_cleaned["Date"], infer_datetime_format=True)
        new_prices_df = new_prices_df.reindex(["Date","Ticker","Open","High","Low","Close","Volume"],axis=1)
        new_prices_df.to_sql("prices_daily", conn, if_exists="append")

        print(f"\n\nUpdating 'prices_daily': {ticker} \n{price_data} \nExisting Prices\n{existing_prices_df} \nLast date: {last_date} \nNew Prices:\n{new_prices_df}")

    def update_symbol(self, ticker, name, exchange):
        try:
            conn = self.connect()
            cursor = conn.cursor()
        except Exception as e:
            print(f"Unable to open connection to database, {e}")
            return
        
        #print(f"Ready to insert {ticker}, {name}, {exchange}")
        try:
            sql = f"SELECT * FROM symbols WHERE ticker = '{ticker.upper()}'"
            result = cursor.execute(sql).fetchone()
        except Exception as e:
            print(f"Unable to read from database, {e}")
            conn.close()
            return
        
        if result is None:
            # Insert into database
            print(f"Ready to INSERT {ticker}, {name}, {exchange}")
            url = f"https://money.tmx.com/en/quote/{ticker}"
            sql = f"INSERT INTO symbols (ticker, name, exchange, url, yahoo) VALUES ('{ticker.upper()}', '{name.upper()}', '{exchange}', '{url}', '-')" 
            #sql = f"INSERT INTO symbols (ticker, name, exchange, url, yahoo) VALUES (?,?,?,?,?)"
            cursor.execute(sql)
            conn.commit()
        else:
            #url = f"https://money.tmx.com/en/quote/{ticker}"
            print(f"Ready to UPDATE {ticker}, {name}, {exchange}")
            sql = f"UPDATE symbols SET name='{name.upper()}', exchange='{exchange}' WHERE ticker = '{ticker.upper()}'"
            cursor.execute(sql)
            conn.commit()
        
        conn.close()

    def get_symbols(self, filter=None):
        """ Open symbols table and return a pandas dataframe of symbols, apply filter on ticker column if not None """
        
        # Open a connection to DB
        conn = self.connect()
        if conn is None:
            return "Connection failed"

        # Setup SQL request 
        sql = f"SELECT * FROM symbols "
        sql_filter = " "
        sql_sort = "ORDER BY ticker ASC"
        if filter is not None:
            filter = f" WHERE ticker LIKE '{filter}%'"
        
        # Extract symbols data from database
        symbols_df = pd.read_sql_query(sql+sql_filter+sql_sort, conn)
        symbols_df.drop("index", axis=1, inplace=True)
        conn.close()
        return symbols_df
        
