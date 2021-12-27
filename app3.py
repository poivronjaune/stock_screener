# Color references : https://www.tcl.tk/man/tcl/TkCmd/colors.html

import time
from typing import Text
import re
import pandas as pd
import tkinter as tk

from tkinter.constants import BOTTOM, TOP, LEFT, RIGHT
from dataclasses import field
from tkinter import Button, Label, Menu, Scrollbar, ttk

from stocksdata import StocksData
from tmx_scraper import TMXScraper

stocks_data = StocksData(db=".\TSX_Prices.sqlite")

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

def root_show_symbols():
    print("Show Symbols menu pressed")
    symbols_main_frame.tkraise()

def root_show_indicators():
    print("Show indicators menu pressed")
    indictaors_main_frame.tkraise()

# DISPLAY a menu on root window
main_menu = tk.Menu(root)
main_menu.add_cascade(label="Statistics", command=root_show_stats)
main_menu.add_cascade(label="Symbols", command=root_show_symbols)
main_menu.add_cascade(label="Indicators", command=root_show_indicators)
main_menu.add_command(label="Quit", command=root.destroy)
root.configure(menu=main_menu)

# FRAMES to display when menus are clicked
stats_main_frame = tk.Frame(root, bg="black")
stats_main_frame.columnconfigure(0, weight=1)
stats_main_frame.columnconfigure(1, weight=1)
stats_main_frame.columnconfigure(2, weight=1)
stats_main_frame.rowconfigure(2, weight=1)

symbols_main_frame = tk.Frame(root, bg="red")
symbols_main_frame.columnconfigure(0, weight=1)
symbols_main_frame.rowconfigure(0, weight=1)

indictaors_main_frame = tk.Frame(root, bg="blue")

# Create all frames on root window and place stats_main_frame on top using tkraise()
stats_main_frame.grid(row=0, column=0, sticky="nsew")
symbols_main_frame.grid(row=0, column=0, sticky="nsew")
indictaors_main_frame.grid(row=0, column=0, sticky="nsew")
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

symbols_stats_frame = tk.LabelFrame(stats_main_frame, text="Symbols statistics", bg=BACKGROUND, fg=WHITE)
tk.Label(symbols_stats_frame, text="SYMBOLS",              bg=BACKGROUND, fg=WHITE ).grid(row=0,column=0, padx=5, pady=5, sticky="w")
tk.Label(symbols_stats_frame, text="Total symbols",        bg=BACKGROUND, fg=WHITE ).grid(row=1,column=0, padx=5, sticky="w")
tk.Label(symbols_stats_frame, text=": ",                   bg=BACKGROUND, fg=WHITE ).grid(row=1,column=1, padx=5, sticky="w")
tk.Label(symbols_stats_frame, textvariable=db_symbols_var, bg=BACKGROUND, fg=WHITE ).grid(row=1,column=2, padx=5, sticky="w")
tk.Label(symbols_stats_frame, text="TSX symbols",          bg=BACKGROUND, fg=WHITE ).grid(row=2,column=0, padx=5, sticky="w")
tk.Label(symbols_stats_frame, text=": ",                   bg=BACKGROUND, fg=WHITE ).grid(row=2,column=1, padx=5, sticky="w")
tk.Label(symbols_stats_frame, textvariable=db_tsx_var,     bg=BACKGROUND, fg=WHITE ).grid(row=2,column=2, padx=5, sticky="w")
tk.Label(symbols_stats_frame, text="TSXV symbols",         bg=BACKGROUND, fg=WHITE ).grid(row=3,column=0, padx=5, sticky="w")
tk.Label(symbols_stats_frame, text=": ",                   bg=BACKGROUND, fg=WHITE ).grid(row=3,column=1, padx=5, sticky="w")
tk.Label(symbols_stats_frame, textvariable=db_tsxv_var,    bg=BACKGROUND, fg=WHITE ).grid(row=3,column=2, padx=5, sticky="w")
symbols_stats_frame.grid(row=0, column=1, padx=5, pady=5, ipadx=3, ipady=3, sticky="nsew")

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
#print(df1)

def update_tree_view(trv, rows_df):
    for item in trv.get_children():
        trv.delete(item)    
    for index, row in rows_df.iterrows():
        trv.insert("", tk.END, iid=index, values=list(row))


def cmd_count():
    global df1
    working_frame.tkraise()
    root.update()
    #df_count = stocks_data.count_prices_per_ticker()
    df1 = stocks_data.count_prices_per_ticker()
    update_tree_view(trv1, df1)
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

def cmd_row_info():
    selected_index = trv1.selection()[0]
    row_values = trv1.item(selected_index, 'values')
    print(f"Row selected : {row_values}")
    print(type(row_values[4]))
    pass

def cmd_treeview_sort(treeview, col, reverse, tv_headings):
    global df1

    df1.sort_values(df1.columns[col-1], ascending=not reverse, inplace=True)
    update_tree_view(treeview, df1)
    treeview.heading(col, command=lambda c=col: cmd_treeview_sort(treeview, c, not reverse, tv_headings))

    # RESET header text to remove sort arrow indicator
    for index, heading_string in enumerate(tv_headings):
        treeview.heading(index+1, text=heading_string)
    
    # SET sort arrow indicator on clicked column
    if reverse:
        treeview.heading(col, text=tv_headings[col-1] + u" \u25B2")
    else:
        treeview.heading(col, text=tv_headings[col-1] + u" \u25BC")


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
# trv1.heading(1, text="Ticker",       command=lambda col=1: treeview_sort_column(trv1, col, False, trv1_headings))
# trv1.heading(2, text="Company Name", command=lambda col=2: treeview_sort_column(trv1, col, False, trv1_headings))
# trv1.heading(3, text="Start Date",   command=lambda col=3: treeview_sort_column(trv1, col, False, trv1_headings))
# trv1.heading(4, text="End Date",     command=lambda col=4: treeview_sort_column(trv1, col, False, trv1_headings))
# trv1.heading(5, text="Price Rows",   command=lambda col=5: treeview_sort_column(trv1, col, False, trv1_headings))
trv1.heading(1, text="Ticker",       command=lambda col=1: cmd_treeview_sort(trv1, col, False, trv1_headings))
trv1.heading(2, text="Company Name", command=lambda col=2: cmd_treeview_sort(trv1, col, False, trv1_headings))
trv1.heading(3, text="Start Date",   command=lambda col=3: cmd_treeview_sort(trv1, col, False, trv1_headings))
trv1.heading(4, text="End Date",     command=lambda col=4: cmd_treeview_sort(trv1, col, False, trv1_headings))
trv1.heading(5, text="Price Rows",   command=lambda col=5: cmd_treeview_sort(trv1, col, False, trv1_headings))

# Create a scroll bar object ot add to our treeview
trv1_scroll = Scrollbar(tree_frame, orient="vertical", command=trv1.yview)
trv1.configure(yscrollcommand=trv1_scroll.set)

update_tree_view(trv1, df1)
trv1.grid(row=0,column=0, sticky="nwes")
trv1_scroll.grid(row=0,column=1, sticky="wns")

buttons_frame = tk.Label(tree_frame, bg=BACKGROUND, fg=WHITE)
tk.Button(buttons_frame,text="Update Count", command=cmd_count).grid(row=1,column=0, sticky="w", padx=3)
tk.Button(buttons_frame,text="Update Prices", command=cmd_update_prices).grid(row=1,column=1, sticky="w", padx=3)
tk.Button(buttons_frame,text="Row info", command=cmd_row_info).grid(row=1,column=2, sticky="w", padx=3)

buttons_frame.grid(row=1, column=0, columnspan=2)

tree_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nesw")
#
#  GUI Preparation for stats_main_frame <END>
###################################################################################


###################################################################################
#
#  GUI Preparation for symbols_main_frame
#
# Get the list of all tickers in our symbols table (not the prices_daily table)
symbols_df = stocks_data.get_symbols()
trv2_df = symbols_df.copy(deep=True)

# Status Bar Tracking Variables
symbols_status_info   = tk.StringVar()
symbols_filter_info   = tk.StringVar()
symbols_selected_info = tk.StringVar()

# Flter frame tracking variables
filter_ticker_str          = tk.StringVar()
filter_company_str         = tk.StringVar()
filter_extraction_symbols  = tk.StringVar()
filter_extraction_exchange = tk.StringVar()

def update_trv2(trv, rows_df):
    for item in trv.get_children():
        trv.delete(item)    
    for index, row in rows_df.iterrows():
        trv.insert("", tk.END, iid=index, values=list(row))

def cmd_trv2_sort(treeview, col, reverse, tv_headings):
    #symbols_df.sort_values(symbols_df.columns[col-1], ascending=not reverse, inplace=True)
    trv2_df.sort_values(trv2_df.columns[col-1], ascending=not reverse, inplace=True)
    update_trv2(treeview, trv2_df)
    treeview.heading(col, command=lambda c=col: cmd_trv2_sort(treeview, c, not reverse, tv_headings))

    # RESET header text to remove sort arrow indicator
    for index, heading_string in enumerate(tv_headings):
        treeview.heading(index+1, text=heading_string)
    
    # SET sort arrow indicator on clicked column
    if reverse:
        treeview.heading(col, text=tv_headings[col-1] + u" \u25B2")
    else:
        treeview.heading(col, text=tv_headings[col-1] + u" \u25BC")

def cmd_trv2_apply_filter():
    ticker_filter = filter_ticker_str.get()
    company_filter = filter_company_str.get()
    if ticker_filter != "":
        end_pos = len(ticker_filter)
        #filtered_df = symbols_df.loc[symbols_df["ticker"].str.contains(ticker_filter)]
        filtered_df = symbols_df.loc[symbols_df["ticker"].str[0:end_pos] == ticker_filter].copy(deep=True)
    elif company_filter != "":
        #end_pos = len(company_filter)
        filtered_df = symbols_df.loc[symbols_df["name"].str.contains(company_filter)].copy(deep=True)
        #filtered_df = symbols_df.loc[symbols_df["name"].str[0:end_pos] == company_filter]
    else:
        filtered_df = symbols_df.copy(deep=True)

    # Set filtered data to trv2_df and display filtered data
    if ticker_filter != "" or company_filter != "":
        trv2_df = filtered_df.copy(deep=True)
        update_trv2(trv2, trv2_df)
        status_update_filtered()

    # print(f"Search applied... [{filter_ticker_str.get()}, {filter_company_str.get()}]")

def cmd_trv2_clear_filter():
    symbols_df = stocks_data.get_symbols()
    filter_ticker_str.set("")
    filter_company_str.set("")
    trv2_df = symbols_df.copy(deep=True)
    update_trv2(trv2, trv2_df)
    symbols_filter_info.set("")
    symbols_selected_info.set("")
    # print(f"Cleared search filter entry fields, and updated the treeview")

def cmd_trv2_extract_and_update_symbols():
    letter   = filter_extraction_symbols.get()
    exchange = filter_extraction_exchange.get()
    if letter != "" and exchange != "":
        symbols_working_msg.tkraise()
        root.update()
        print(f"Lauching extraction using Selenium for letter {letter}....")
        tmx_scraper = TMXScraper()
        data = tmx_scraper.scrap_symbols(letter, exchange)
        if data is not None:
            print(data)
            for index,row in data.iterrows():
                ticker_str   = row["ticker"]
                name_str     = row["company"].replace("'"," ")
                exchange_str = row["exchange"]
                print(f"{index} : {ticker_str}, {name_str}, {exchange_str}")
                stocks_data.update_symbol(ticker_str, name_str, exchange_str)
                #stocks_data.update_symbol(row["ticker"], row["company"], row["exchange"])                
        else:
            print("No data extracted...")
        
        symbols_df = stocks_data.get_symbols()
        trv2_df = symbols_df.copy(deep=True)
        update_tree_view(trv2, trv2_df)
        trv2_container.tkraise()
        root.update()

def cmd_trv2_selected_event(a):
    selected_items = trv2.selection()
    symbols_selected_info.set(f"selected : {len(selected_items)}")

def status_update_totals():
    total_symbols = symbols_df.shape[0]
    total_tsx     = symbols_df.loc[symbols_df["exchange"] == "tsx"].shape[0]
    total_tsxv    = symbols_df.loc[symbols_df["exchange"] == "tsxv"].shape[0]
    symbols_status_info.set(f"Symbols : {total_symbols} | (tsx, tsxv) : ({total_tsx},{total_tsxv})")

def status_update_filtered():
    filtered_symbols = trv2_df.shape[0]
    filtered_tsx     = trv2_df.loc[trv2_df["exchange"] == "tsx"].shape[0]
    filtered_tsxv    = trv2_df.loc[trv2_df["exchange"] == "tsxv"].shape[0]
    symbols_filter_info.set(f"Filtered symbols : {filtered_symbols} | (tsx, tsxv) : ({filtered_tsx},{filtered_tsxv})")


symbols_frame = tk.LabelFrame(symbols_main_frame, text="Symbols", bg=BACKGROUND, fg=WHITE)
symbols_frame.columnconfigure(0, weight=1)
symbols_frame.rowconfigure(1, weight=1)

filter_frame = tk.LabelFrame(symbols_frame, text="Filters", bg=BACKGROUND, fg=WHITE)
tk.Label(filter_frame, text="Ticker : ", bg=BACKGROUND, fg=WHITE).grid(row=0, column=0)
tk.Entry(filter_frame, textvariable=filter_ticker_str).grid(row=0, column=1, padx=10, pady=5)
tk.Label(filter_frame, text="Company : ", bg=BACKGROUND, fg=WHITE).grid(row=0, column=2)
tk.Entry(filter_frame, textvariable=filter_company_str).grid(row=0, column=3, padx=10, pady=5)
tk.Button(filter_frame, text="Apply", command=cmd_trv2_apply_filter).grid(row=0,column=5, padx=10, pady=10)
tk.Button(filter_frame, text="Clear", command=cmd_trv2_clear_filter).grid(row=0,column=6, padx=10)
letter_choices = ttk.Combobox(filter_frame, textvariable=filter_extraction_symbols, width=5)
letter_choices["values"] = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
letter_choices["state"]  = "readonly"
letter_choices.grid(row=0, column=7)
exchange_choices = ttk.Combobox(filter_frame, textvariable=filter_extraction_exchange, width=5)
exchange_choices["values"] = ["tsx","tsxv"]
exchange_choices["state"]  = "readonly"
exchange_choices.grid(row=0, column=8)
tk.Button(filter_frame, text="Update", command=cmd_trv2_extract_and_update_symbols).grid(row=0,column=9, padx=10)
filter_frame.grid(row=0, column=0, sticky="ew")

# Add a widget behind Treeview and raise it up when long running processes are executed
symbols_working_msg = tk.Label(symbols_frame, text=f"Working Please wait...\nA Chrome Browser will open to extract data, please wait until it closes.", bg=BACKGROUND, fg=WHITE)
symbols_working_msg.grid(row=1,column=0,sticky="nsew")

# STYLE for our Treeview
trv2_container = tk.Frame(symbols_frame)
trv2_container.rowconfigure(0, weight=1)
trv2_container.columnconfigure(0, weight=1)

trv2_style = ttk.Style()
trv2_style.theme_use("default")
trv2_style.configure("Treeview",
    background = BACKGROUND,
    foreground = WHITE,
    fieldbackground = BACKGROUND
)
trv2_style.map("Treeview", [("selected", "GREEN")])

trv2 = ttk.Treeview(trv2_container, columns=(1,2,3,4,5), show="headings", height="6")
trv2_headings = ["Ticker", "Company Name", "Exchange", "URL", "Yahoo"]
trv2.heading(1, text="Ticker",      command=lambda col=1: cmd_trv2_sort(trv2, col, False, trv2_headings))
trv2.heading(2, text="Company Name",command=lambda col=2: cmd_trv2_sort(trv2, col, False, trv2_headings))
trv2.heading(3, text="Exchange",    command=lambda col=3: cmd_trv2_sort(trv2, col, False, trv2_headings))
trv2.heading(4, text="URL",         command=lambda col=4: cmd_trv2_sort(trv2, col, False, trv2_headings))    
trv2.heading(5, text="Yahoo",       command=lambda col=5: cmd_trv2_sort(trv2, col, False, trv2_headings))
trv2.bind('<ButtonRelease-1>', cmd_trv2_selected_event)

trv2_scroll = Scrollbar(trv2_container, orient="vertical", command=trv2.yview)
trv2.configure(yscrollcommand=trv2_scroll.set)

# Display treeview on symbols frame
trv2.grid(row=0, column=0, sticky="nsew")
trv2_scroll.grid(row=0,column=1, sticky="wns")
trv2_container.grid(row=1, column=0, sticky="nsew")

# create a status bar at bottom of symbols frame
symbols_status_bar_frame = tk.Frame(symbols_frame)
symbols_status_bar_frame.columnconfigure(0, weight=1)
symbols_status_bar_frame.columnconfigure(1, weight=1)
symbols_status_bar_frame.columnconfigure(2, weight=1)
# l1 = Label(root, text="This", borderwidth=2, relief="groove")
tk.Label(symbols_status_bar_frame, textvariable=symbols_status_info  , borderwidth=2, relief="sunken").grid(row=0, column=0, sticky="ew")
tk.Label(symbols_status_bar_frame, textvariable=symbols_filter_info  , borderwidth=2, relief="sunken").grid(row=0, column=1, sticky="ew")
tk.Label(symbols_status_bar_frame, textvariable=symbols_selected_info, borderwidth=2, relief="sunken").grid(row=0, column=2, sticky="ew")

symbols_status_bar_frame.grid(row=2, column=0, sticky="ew")


# Update widgets data
update_trv2(trv2, trv2_df)
status_update_totals()

symbols_frame.grid(row=0, column=0, sticky="nsew")
root.update()

#  GUI Preparation for symbols_main_frame <END>
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
