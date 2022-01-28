from datetime import datetime
import os
import sqlite3
import pandas as pd
import numpy as np
from finta import TA

import matplotlib as plot
import mplfinance as mpf
import plotly.graph_objects as go
from tenacity import time

#%matplotlib inline

database_name = "TSX_Quality.sqlite"

start_time = datetime.now()
#########################################################################

print(f"Début : {start_time}")
conn = sqlite3.connect(database_name)
symbol = "SHOP"
#SQL = f"SELECT * FROM Indicators WHERE ticker ='{symbol}'"
SQL = f"SELECT * FROM Indicators"
data = pd.read_sql_query(SQL, conn)
print(data)

#########################################################################
print(f"Fin   : {start_time}")
endtime = datetime.now()
print(f"Fin   : {endtime}")
print(f"Durée : {endtime - start_time}")
conn.close()
