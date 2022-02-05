import os
import sqlite3
import pandas as pd
import yfinance as yf

database_name = "..\TSX_Quality.sqlite"

conn = sqlite3.connect(database_name)
sql = f"SELECT * FROM Symbols WHERE exchange='tsxv' ORDER BY UPPER(Ticker) ASC"
symbols_df = pd.read_sql_query(sql, conn)

tsxv_list = []
for symbol in symbols_df["ticker"]:
    yahoo = symbol.replace(".","-") + ".V"
    tsxv_list.append(yahoo)

data = yf.download(tsxv_list, start="2022-01-01", group_by="ticker")
sym_list = [val[0] for val in data.columns]
unique_symbols = list(dict.fromkeys(sym_list))

print(unique_symbols)

sym_str = '{\n"symbols":[\n'
for sym in unique_symbols:
    sym_str = sym_str + f'\t"{sym}",\n'
sym_str = sym_str[0:-2] + "\n  ]\n}"

f = open("TSXVFORYAHOO.json", "a")
f.write(sym_str)
f.close()
