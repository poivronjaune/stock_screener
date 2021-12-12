# Color references : https://www.tcl.tk/man/tcl/TkCmd/colors.html

import time
import pandas as pd
import tkinter as tk

from tkinter.constants import BOTTOM, TOP, LEFT, RIGHT
from dataclasses import field
from tkinter import Button, Label, Menu, Scrollbar, ttk

from stocksdata import StocksData
from tmx_scraper import TMXScraper

stocks_data = StocksData(db=".\TSX_Prices.sqlite")
print(stocks_data)

root = tk.Tk()

# Color scheme
BACKGROUND  = "#131722"
RED         = "#ff4a68"
BLUE        = "#2962ff"
WHITE       = "#D1D4DC"
GREEN       = "#26A69A"

# Root window configuration
root.title(f"TSX Desktop Stocks Screener - {stocks_data.full_path} ")
root.geometry("800x600")
root.state("zoomed")
root.iconbitmap(f".\images\poivronjaune.ico")
root.configure(bg=BACKGROUND)

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

def root_show_stats():
    print("Show statistics menu pressed")
    stats_main_frame.tkraise()

def root_show_indicators():
    print("Show indicators menu pressed")
    Indictaors_main_frame.tkraise()

# DISPLAY a menu on root window
main_menu = tk.Menu(root)
main_menu.add_cascade(label="Statistics", command=root_show_stats)
main_menu.add_cascade(label="Indicators", command=root_show_indicators)
main_menu.add_command(label="Quit", command=root.destroy)
root.configure(menu=main_menu)

# FRAMES to display when menus are clicked
stats_main_frame = tk.Frame(root, bg="red")
stats_main_frame.columnconfigure(0, weight=1)
stats_main_frame.columnconfigure(1, weight=1)
stats_main_frame.columnconfigure(2, weight=1)
stats_main_frame.rowconfigure(2, weight=1)

Indictaors_main_frame = tk.Frame(root, bg="blue")

# Create all frames on root window and place stats_main_frame on top using tkraise()
stats_main_frame.grid(row=0, column=0, sticky="nsew")
Indictaors_main_frame.grid(row=0, column=0, sticky="nsew")
stats_main_frame.tkraise()


########################################################
# StringVars for binding data to widgets
db_name_var    = tk.StringVar()
db_drive_var   = tk.StringVar()
db_path_var    = tk.StringVar()
db_size_var    = tk.StringVar()
db_update_var  = tk.StringVar()
db_type_var    = tk.StringVar()

db_symbols_var = tk.StringVar()
db_tsx_var     = tk.StringVar()
db_tsxv_var    = tk.StringVar()
prices_rows_var    = tk.StringVar()
prices_tickers_var = tk.StringVar()
prices_missing_var = tk.StringVar()



###################################################################################
#
#  GUI Preparation for stats_main_frame
#
#  Widgets for database information
info_frame = tk.LabelFrame(stats_main_frame, text="Database information", bg=BACKGROUND, fg=WHITE)
tk.Label(info_frame, text="Database name",        bg=BACKGROUND, fg=WHITE ).grid(row=0,column=0, padx=5, sticky="w")
tk.Label(info_frame, text=": ",                   bg=BACKGROUND, fg=WHITE ).grid(row=0,column=1, padx=5, sticky="w")
tk.Label(info_frame, textvariable=db_name_var,    bg=BACKGROUND, fg=WHITE ).grid(row=0,column=2, padx=5, sticky="w")
tk.Label(info_frame, text="Database drive",       bg=BACKGROUND, fg=WHITE ).grid(row=1,column=0, padx=5, sticky="w")
tk.Label(info_frame, text=": ",                   bg=BACKGROUND, fg=WHITE ).grid(row=1,column=1, padx=5, sticky="w")
tk.Label(info_frame, textvariable=db_drive_var,   bg=BACKGROUND, fg=WHITE ).grid(row=1,column=2, padx=5, sticky="w")
tk.Label(info_frame, text="Database path",        bg=BACKGROUND, fg=WHITE ).grid(row=2,column=0, padx=5, sticky="w")
tk.Label(info_frame, text=": ",                   bg=BACKGROUND, fg=WHITE ).grid(row=2,column=1, padx=5, sticky="w")
tk.Label(info_frame, textvariable=db_path_var,    bg=BACKGROUND, fg=WHITE ).grid(row=2,column=2, padx=5, sticky="w")
tk.Label(info_frame, text="Database size",        bg=BACKGROUND, fg=WHITE ).grid(row=3,column=0, padx=5, sticky="w")
tk.Label(info_frame, text=": ",                   bg=BACKGROUND, fg=WHITE ).grid(row=3,column=1, padx=5, sticky="w")
tk.Label(info_frame, textvariable=db_size_var,    bg=BACKGROUND, fg=WHITE ).grid(row=3,column=2, padx=5, sticky="w")
tk.Label(info_frame, text="Database type",        bg=BACKGROUND, fg=WHITE ).grid(row=4,column=0, padx=5, sticky="w")
tk.Label(info_frame, text=": ",                   bg=BACKGROUND, fg=WHITE ).grid(row=4,column=1, padx=5, sticky="w")
tk.Label(info_frame, textvariable=db_type_var,    bg=BACKGROUND, fg=WHITE ).grid(row=4,column=2, padx=5, sticky="w")
tk.Label(info_frame, text="Last updated",         bg=BACKGROUND, fg=WHITE ).grid(row=5,column=0, padx=5, sticky="w")
tk.Label(info_frame, text=": ",                   bg=BACKGROUND, fg=WHITE ).grid(row=5,column=1, padx=5, sticky="w")
tk.Label(info_frame, textvariable=db_update_var,  bg=BACKGROUND, fg=WHITE ).grid(row=5,column=2, padx=5, sticky="w")
info_frame.grid(row=0, column=0, padx=5, pady=5, ipadx=3, ipady=3, sticky="nsew")

# Widgets for Symbols Stats information
symbols_frame = tk.LabelFrame(stats_main_frame, text="Symbols statistics", bg=BACKGROUND, fg=WHITE)
tk.Label(symbols_frame, text="SYMBOLS",              bg=BACKGROUND, fg=WHITE ).grid(row=0,column=0, padx=5, pady=5, sticky="w")
tk.Label(symbols_frame, text="Total symbols",        bg=BACKGROUND, fg=WHITE ).grid(row=1,column=0, padx=5, sticky="w")
tk.Label(symbols_frame, text=": ",                   bg=BACKGROUND, fg=WHITE ).grid(row=1,column=1, padx=5, sticky="w")
tk.Label(symbols_frame, textvariable=db_symbols_var, bg=BACKGROUND, fg=WHITE ).grid(row=1,column=2, padx=5, sticky="w")
tk.Label(symbols_frame, text="TSX symbols",          bg=BACKGROUND, fg=WHITE ).grid(row=2,column=0, padx=5, sticky="w")
tk.Label(symbols_frame, text=": ",                   bg=BACKGROUND, fg=WHITE ).grid(row=2,column=1, padx=5, sticky="w")
tk.Label(symbols_frame, textvariable=db_tsx_var,     bg=BACKGROUND, fg=WHITE ).grid(row=2,column=2, padx=5, sticky="w")
tk.Label(symbols_frame, text="TSXV symbols",         bg=BACKGROUND, fg=WHITE ).grid(row=3,column=0, padx=5, sticky="w")
tk.Label(symbols_frame, text=": ",                   bg=BACKGROUND, fg=WHITE ).grid(row=3,column=1, padx=5, sticky="w")
tk.Label(symbols_frame, textvariable=db_tsxv_var,    bg=BACKGROUND, fg=WHITE ).grid(row=3,column=2, padx=5, sticky="w")
symbols_frame.grid(row=0, column=1, padx=5, pady=5, ipadx=3, ipady=3, sticky="nsew")

# Widgets for Prices Stats information
prices_frame = tk.LabelFrame(stats_main_frame, text="Prices statistics", bg=BACKGROUND, fg=WHITE)
tk.Label(prices_frame, text="PRICES",                   bg=BACKGROUND, fg=WHITE ).grid(row=4,column=0, padx=5, pady=5, sticky="w")
tk.Label(prices_frame, text="Prices total rows",        bg=BACKGROUND, fg=WHITE ).grid(row=5,column=0, padx=5, sticky="w")
tk.Label(prices_frame, text=": ",                       bg=BACKGROUND, fg=WHITE ).grid(row=5,column=1, padx=5, sticky="w")
tk.Label(prices_frame, textvariable=prices_rows_var,    bg=BACKGROUND, fg=WHITE ).grid(row=5,column=2, padx=5, sticky="w")
tk.Label(prices_frame, text="Prices tickers count",     bg=BACKGROUND, fg=WHITE ).grid(row=6,column=0, padx=5, sticky="w")
tk.Label(prices_frame, text=": ",                       bg=BACKGROUND, fg=WHITE ).grid(row=6,column=1, padx=5, sticky="w")
tk.Label(prices_frame, textvariable=prices_tickers_var, bg=BACKGROUND, fg=WHITE ).grid(row=6,column=2, padx=5, sticky="w")
tk.Label(prices_frame, text="Prices missing tickers",   bg=BACKGROUND, fg=WHITE ).grid(row=7,column=0, padx=5, sticky="w")
tk.Label(prices_frame, text=": ",                       bg=BACKGROUND, fg=WHITE ).grid(row=7,column=1, padx=5, sticky="w")
tk.Label(prices_frame, textvariable=prices_missing_var, bg=BACKGROUND, fg=WHITE ).grid(row=7,column=2, padx=5, sticky="w")
prices_frame.grid(row=0, column=2, padx=5, pady=5, ipadx=3, ipady=3, sticky="nsew")

# WORKING Frame to display when a long process is running
working_frame = tk.LabelFrame(stats_main_frame, text="Number of prices per ticker symbol", bg=BACKGROUND, fg=WHITE)
tk.Label(working_frame, text="Working Please wait...", bg=BACKGROUND, fg=WHITE).pack(expand="yes", fill=tk.BOTH)
working_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nesw")

# UTILTY FUNCTIONS FOR Treeview
df1 = stocks_data.count_prices_per_ticker(count=False) # Return an empty data_frame since count=False.
print(df1)

def update_tree_view(trv, rows_df):
    for item in trv.get_children():
        trv.delete(item)    
    for index, row in rows_df.iterrows():
        trv.insert("", tk.END, iid=index, values=list(row))


def cmd_count():
    working_frame.tkraise()
    root.update()
    df_count = stocks_data.count_prices_per_ticker()
    update_tree_view(trv1, df_count)
    tree_frame.tkraise()
    root.update()


def cmd_update_prices():
    """ Scrap data from tree_list view containing ticker symbols """

    trv1_rows_selected = trv1.selection()
    if len(trv1_rows_selected) > 0:
        tmx_scraper = TMXScraper()
        for trv1_row_selected in trv1_rows_selected:
            row_data = trv1.item(trv1_row_selected)['values']
            trv1.selection_set(trv1_row_selected)
            trv1.see(trv1_row_selected)
            root.update()
            ticker = row_data[0]
            df_prices_from_html = tmx_scraper.scrap_pages(ticker, pages=1)
            stocks_data.update_prices_daily(ticker, df_prices_from_html)
        tmx_scraper.close()

def treeview_sort_column(treeview, col, reverse, tv_headings):
    """ Sort a treeview column clicked """
    data = [ (treeview.set(iid, col), iid) for iid in treeview.get_children("") ]
    data.sort(reverse=reverse)

    for index, (sort_val, iid) in enumerate(data):
        treeview.move(iid, "", index)

    treeview.heading(col, command=lambda c=col: treeview_sort_column(treeview, c, not reverse, tv_headings))

    # RESET header text to remove sort arrow indicator
    for index, heading_string in enumerate(tv_headings):
        treeview.heading(index+1, text=heading_string)
    
    # SET sort arrow indicator on clicked column
    if reverse:
        treeview.heading(col, text=tv_headings[col-1] + u" \u25B2")
    else:
        treeview.heading(col, text=tv_headings[col-1] + u" \u25BC")



tree_frame = tk.LabelFrame(stats_main_frame, text="Number of prices per ticker symbol", bg=BACKGROUND, fg=WHITE)
tree_frame.columnconfigure(0, weight=1)
tree_frame.rowconfigure(0, weight=1)

# STYLE for our Treeview
trv1_style = ttk.Style()
trv1_style.theme_use("default")
trv1_style.configure("Treeview",
    background = BACKGROUND,
    foreground = WHITE,
    fieldbackground = BACKGROUND
)
trv1_style.map("Treeview", [("selected", "GREEN")])

# Create our treeview widget with specific columns, and add scroll bar
trv1 = ttk.Treeview(tree_frame, columns=(1,2,3,4,5), show="headings", height="6")
trv1_headings = ["Ticker", "Company Name", "Start Date", "End Date", "Price Rows"]
trv1.heading(1, text="Ticker",       command=lambda col=1: treeview_sort_column(trv1, col, False, trv1_headings))
trv1.heading(2, text="Company Name", command=lambda col=2: treeview_sort_column(trv1, col, False, trv1_headings))
trv1.heading(3, text="Start Date",   command=lambda col=3: treeview_sort_column(trv1, col, False, trv1_headings))
trv1.heading(4, text="End Date",     command=lambda col=4: treeview_sort_column(trv1, col, False, trv1_headings))
trv1.heading(5, text="Price Rows",   command=lambda col=5: treeview_sort_column(trv1, col, False, trv1_headings))

# Create a scroll bar object ot add to our treeview
trv1_scroll = Scrollbar(tree_frame, orient="vertical", command=trv1.yview)
trv1.configure(yscrollcommand=trv1_scroll.set)

update_tree_view(trv1, df1)
trv1.grid(row=0,column=0, sticky="nwes")
trv1_scroll.grid(row=0,column=1, sticky="wns")

buttons_frame = tk.Label(tree_frame, bg=BACKGROUND, fg=WHITE)
tk.Button(buttons_frame,text="Update Count", command=cmd_count).grid(row=1,column=0, sticky="w", padx=3)
tk.Button(buttons_frame,text="Update Prices", command=cmd_update_prices).grid(row=1,column=1, sticky="w", padx=3)
buttons_frame.grid(row=1, column=0, columnspan=2)

tree_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nesw")
#
#  GUI Preparation for stats_main_frame <END>
###################################################################################


###################################################################################
#
#  GUI Preparation for indicators_main_frame



#
#  GUI Preparation for indicators_main_frame <END>
###################################################################################


# Update all Database information using widget contol varaibles that are binded to each stats widget
db_name_var.set(f"{stocks_data.filename}")
db_drive_var.set(f"{stocks_data.drive}")
db_path_var.set(f"{stocks_data.path}")
size_str = '{:,.2f}'.format(stocks_data.db_size / 1024).replace(',', ' ')
db_size_var.set(f"{size_str } Kb")
db_type_var.set(f"{stocks_data.db_type}")
db_update_var.set(f"{stocks_data.last_update}")

# Update all stats information
db_symbols_var.set(f"{stocks_data.count_symbols}")
db_tsx_var.set(f"{stocks_data.count_tsx}")     
db_tsxv_var.set(f"{stocks_data.count_tsxv}")

rows_str = '{:,}'.format(stocks_data.stats_prices).replace(',', ' ')
prices_rows_var.set(f"{rows_str}")   
ticker_str = '{:,}'.format(stocks_data.stats_tickers).replace(',', ' ')
prices_tickers_var.set(f"{ticker_str}")   
missing_str = '{:,}'.format(stocks_data.stats_missing).replace(',', ' ')
prices_missing_var.set(f"{missing_str}")   


# Run main loop of Tkinter GUI 
root.mainloop()
