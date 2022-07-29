from flask import Flask, request, redirect, render_template, url_for, jsonify, make_response, flash, redirect,url_for,session,logging,request
import yfinance as yf
from decimal import Decimal
# import requests module
import requests
import cffi
from jinja2 import escape
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import df2gspread as d2g
import requests
#import schedule
import pandas as pd
#import time
import optparse
import os
from fake_useragent import UserAgent
#import pyuser_agent
from decimal import Decimal
import json
import schedule
import time
from datetime import datetime, timedelta
import ftplib
import csv
import random
import pandas as pd
import numpy as np

app = Flask('app')

@app.route('/', methods = ['GET', 'POST'])
def home():
    if(request.method == 'GET'):
  
        data = "hello world"
        return jsonify({'data': data})

#@app.route('/key/<x>', methods = ['GET', 'POST'])
#def key(x):
 #   if(request.method == 'GET'):
 #       #symbol = request.args.get('symbol', x)
 #       getinformation = yf.Ticker(x)
 
# get all key value pairs that are available
  #      for key, value in getinformation.info.items():
  #        data = (key, ":", value)
  #      return data
@app.route('/ystocks', methods = ['GET', 'POST'])
def ystocks():
    if(request.method == 'GET'):
      #Reading a file from  ftp server
      # Fill Required Information
      HOSTNAME = "74.208.51.69"
      USERNAME = "stockftpusr"
      PASSWORD = "T11wz8w_"

      # Connect FTP Server
      ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)

      # force UTF-8 encoding
      ftp_server.encoding = "utf-8"
      ftp_server.cwd('/assets/yahoo/most_active/')
      # Get list of files
      ftp_server.dir() 
      # Enter File Name with Extension
      filename = "yahoo_most_active1.csv"

      # Write file in binary mode
      with open(filename, "wb") as file:
        # Command for Downloading the file "RETR filename"
        ftp_server.retrbinary(f"RETR {filename}", file.write)

      # Get list of files
      ftp_server.dir()

# Display the content of downloaded file
#file= open(filename, "r")
#print('File Content:', file.read())

      # Close the Connection
      ftp_server.quit()
      #
      # reading a second row in csv
      noise_amp=[]         #an empty list to store the second column
      with open('yahoo_most_active1.csv', 'r') as rf:
        reader = csv.reader(rf, delimiter=',')
        for row in reader:
          noise_amp.append(row[1])
          # which row we need to read , 1 is frist row , 2 is second row
         #print(noise_amp)
      urls=noise_amp[1:10]
      shortName = []
      symbol = []
      volume = []
      currentPrice = []
      averageVolume = []
      previousClose = []
      for url in urls:
        tickerTag = yf.Ticker(url)
        shortName.append(tickerTag.info['shortName'])
        symbol.append(tickerTag.info['symbol'])
        volume.append(tickerTag.info['volume'])
        currentPrice.append(tickerTag.info['currentPrice'])
        averageVolume.append(tickerTag.info['averageVolume'])
        previousClose.append(tickerTag.info['previousClose'])
      data = [shortName, symbol, volume, currentPrice, averageVolume, previousClose,]
      df = pd.DataFrame(columns=[noise_amp[1:10]], data=data)
      df.to_csv('data.csv')
      data = "hello world"
      return jsonify({'data': data})

###
###
###

@app.route('/info/', methods =["GET", "POST"])
def display_quote():
    if request.method == "POST":
        # getting input with name = fname in HTML form
        x = request.form['text']
    
        symbol = request.args.get('symbol', x)

        quote = yf.Ticker(symbol)

        return quote.info
        #return redirect(url_for("datas",  x=x))
    else:
        return render_template("forms.html")

@app.route("/info/<x>", methods =["GET", "POST"])
def datas(x):
    #x = request.form['text']
    symbol = request.args.get('symbol', x)
 
    quote = yf.Ticker(symbol)
    return quote.info




@app.route("/history", methods =["GET", "POST"])
def display_history():
    if request.method == "POST":
        # getting input with name = fname in HTML form
        text = request.form['text']

        symbol = request.args.get('symbol', text)
        period = request.args.get('period', default="1y")
        interval = request.args.get('interval', default="1mo")        
        quote = yf.Ticker(symbol)   
        hist = quote.history(period=period, interval=interval)
        data = hist.to_json()
        return data
    return render_template("history.html")

@app.route("/historydata/<x>")
def history(x):
    #x = request.form['text']
    symbol = request.args.get('symbol', x)
    period = request.args.get('period', default="1y")
    interval = request.args.get('interval', default="1mo")        
    quote = yf.Ticker(symbol)   
    hist = quote.history(period=period, interval=interval)
    data = hist.to_json()
    return data

@app.route("/stockdata", methods =["GET", "POST"])
def display_data():
     if request.method == "POST":
        # getting input with name = fname in HTML form
        text = request.form['text']
        symbol = request.args.get('symbol', text)
        quote = yf.Ticker(symbol)
#start = datetime.datetime(2018,1,1)
#end = datetime.datetime(2019,7,17)
#data = yf.download(stocks, start=start, end=end)
   # a = quote.info['shortName']
    #b = quote.info['symbol']
   # c = quote.info['currentPrice']
   # d = quote.info['profitMargins']
   # e = quote.info['volume']
   # f = quote.info['averageVolume']
   # g = quote.info['marketCap']
    #h = quote.info['trailingPE']
    #i = (a, b, c, d, e, f, g, h)
        return {
   "company_name": quote.info['shortName'],
   "company_symbol": quote.info['symbol'],
   "current_price": quote.info['currentPrice'],
   "profit_margins": quote.info['profitMargins'],
   "volume": quote.info['volume'],
   "average_volume": quote.info['averageVolume'],
   "marketcap": quote.info['marketCap'],
    }
     return render_template("data.html")

@app.route("/stock/<x>")
def invidual(x):
    #x = request.form['text']
    #text = request.form['text']
    symbol = request.args.get('symbol', x)
    quote = yf.Ticker(symbol)
    name = quote.info['shortName']
    symbol = quote.info['symbol']
    price = quote.info['currentPrice']
    margin = quote.info['profitMargins']
    volume = quote.info['volume']
    avg_vloume = quote.info['averageVolume']
    mkt_cap = quote.info['marketCap']
    value = '1'
    #r = requests.get('https://testing.mobilteam.repl.co/stock/amd')
    data = [{
   "company_name": name,
   "company_symbol": symbol,
   "current_price": price,
   "profit_margins": margin,
   "volume": volume,
   "average_volume": avg_vloume,
   "marketcap": mkt_cap,
    }]
    return jsonify({
      'code': value,
      #'status': r.status_code,
      'data': data})


@app.route("/stocks/<x>")
def stock_test(x):
    #x = request.form['text']
    #text = request.form['text']
    symbol = request.args.get('symbol', x)
    quote = yf.Ticker(symbol)
    value = '2'
    a = Decimal(quote.info['currentPrice'])
    b = Decimal(quote.info['previousClose'])
    change = round((a-b), 2)
    # (New Price - Old Price) / Old Price x 100
    d = round((((a-b)/b)*100), 2)
    #r = requests.get('https://testing.mobilteam.repl.co/stock/amd')
    data = [{
   "company_name": quote.info['shortName'],
   "company_symbol": quote.info['symbol'],
   "current_price": quote.info['currentPrice'],
   #"profit-margins": quote.info['profitMargins'],
   "volume": quote.info['volume'],
   "average_volume": quote.info['averageVolume'],
   #"marketcap": quote.info['marketCap'],
   #"52_weeks_company_range_min": quote.info['fiftyTwoWeekLow'],
   #"52_weeks_company_range_max": quote.info['fiftyTwoWeekHigh'],
   #"days_range_min": quote.info['dayLow'],
   #"days_range_max": quote.info['dayHigh'],
   "Previous_close": quote.info['previousClose'],
   "change": change,
   "change_percentage": d,
    }]
    return jsonify({
      'code': value,
      #'status': r.status_code,
      'data': data})

@app.route("/invidual-stock/<x>")
def data_test(x):
    #x = request.form['text']
    #text = request.form['text']
    symbol = request.args.get('symbol', x)
    quote = yf.Ticker(symbol)
    value = '2'
    a = Decimal(quote.info['currentPrice'])
    b = Decimal(quote.info['previousClose'])
    change = round((a-b), 2)
    # (New Price - Old Price) / Old Price x 100
    d = round((((a-b)/b)*100), 2)
    #r = requests.get('https://testing.mobilteam.repl.co/stock/amd')
    data = [{
   "company_name": quote.info['shortName'],
   "company_symbol": quote.info['symbol'],
   "current_price": quote.info['currentPrice'],
   "profit-margins": quote.info['profitMargins'],
   "volume": quote.info['volume'],
   "average_volume": quote.info['averageVolume'],
   "marketcap": quote.info['marketCap'],
   "52_weeks_company_range_min": quote.info['fiftyTwoWeekLow'],
   "52_weeks_company_range_max": quote.info['fiftyTwoWeekHigh'],
   "days_range_min": quote.info['dayLow'],
   "days_range_max": quote.info['dayHigh'],
   "Previous_close": quote.info['previousClose'],
   "change": change,
   "change_percentage": d,
    }]
    return jsonify({
      'code': value,
      #'status': r.status_code,
      'data': data})


@app.route("/gainersfile", methods =["GET", "POST"])
def gainersdatas():
    if request.method == "POST":
        if True:
            url = request.form['text']
            # getting input with name = fname in HTML form
            #ua = pyuser_agent.UA()
            ua = UserAgent()
            #url = request.form['namee']
            #url = 'https://finance.yahoo.com/gainers?count=100&offset=0'
            headers = {'User-Agent': ua.random }
            html = requests.get(url, headers=headers).content
        #html = requests.get(url).content
            soup = BeautifulSoup(html, 'lxml')
            ac = soup.find_all('a', attrs={'data-test': 'quoteLink'})
            bc = soup.find_all('td', attrs={'aria-label': 'Name'})
            cc = soup.find_all('td', attrs={'aria-label': 'Price (Intraday)'})
            dc = soup.find_all('td', attrs={'aria-label': 'Change'})
            ec = soup.find_all('td', attrs={'aria-label': '% Change'})
            fc = soup.find_all('td', attrs={'aria-label': 'Volume'})
            gc = soup.find_all('td', attrs={'aria-label': 'Avg Vol (3 month)'})
            hc = soup.find_all('td', attrs={'aria-label': 'Market Cap'})
            ic = soup.find_all('td', attrs={'aria-label': 'PE Ratio (TTM)'})
  

            ac_ = []
            bc_ = []
            cc_ = []
            dc_ = []
            ec_ = []
            fc_ = []
            gc_ = []
            hc_ = []
            ic_ = []
            for title in ac:
                ac_.append(title.text.strip())
            for title in bc:
                bc_.append(title.text.strip())
            for title in cc:
                cc_.append(title.text.strip())
            for title in dc:
                dc_.append(title.text.strip())
            for title in ec:
                ec_.append(title.text.strip())
            for title in fc:
                fc_.append(title.text.strip())
            for title in gc:
                gc_.append(title.text.strip())
            for title in hc:
                hc_.append(title.text.strip())
            for title in ic:
                ic_.append(title.text.strip())
  # dataframe Name and Age columns
            df = pd.DataFrame({'Symbol': ac_, 'Name': bc_, 'Price': cc_, 'Change': dc_, 'Change %': ec_, 'Volume': fc_, 'Avg volume': gc_, 'Market cap': hc_, 'Ration': ic_,})
            scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/spreadsheets']
            creds = ServiceAccountCredentials.from_json_keyfile_name('s.json', scope)
            client = gspread.authorize(creds)
            spreadsheet_key = '1m-mrYAqoUvm5OTN1dq8rRr3sLtDuEh8bxVzQCYi2q44'
            wks_name = 'Sheet1'
            cell_of_start_df = 'A2'
            d2g.upload(df,
            spreadsheet_key,
            wks_name,
            credentials=creds,
            col_names=False,
            row_names=False,
            start_cell = cell_of_start_df,
            clean=False)
            requests.get("https://stocks.desss-portfolio.com/yahoo/yahoo_gainers")
          #  return schedule.CancelJob
            return 'ok'
    #schedule.every(1).seconds.do(gainersdatas)
    #while True:
    #    schedule.run_pending()
    #    if not schedule.jobs:
    #        break
    #    time.sleep(1)
    return render_template("gainers4.html")

user_agent_nasdaq = [
'Mozilla/5.0 (Amiga; U; AmigaOS 1.3; en; rv:1.8.1.19) Gecko/20081204 SeaMonkey/1.1.14', 
'Mozilla/5.0 (AmigaOS; U; AmigaOS 1.3; en-US; rv:1.8.1.21) Gecko/20090303 SeaMonkey/1.1.15', 
'Mozilla/5.0 (AmigaOS; U; AmigaOS 1.3; en; rv:1.8.1.19) Gecko/20081204 SeaMonkey/1.1.14', 
'Mozilla/5.0 (Android 2.2; Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4', 
'Mozilla/5.0 (BeOS; U; BeOS BeBox; fr; rv:1.9) Gecko/2008052906 BonEcho/2.0', 
'Mozilla/5.0 (BeOS; U; BeOS BePC; en-US; rv:1.8.1.1) Gecko/20061220 BonEcho/2.0.0.1', 
'Mozilla/5.0 (BeOS; U; BeOS BePC; en-US; rv:1.8.1.10) Gecko/20071128 BonEcho/2.0.0.10', 
'Mozilla/5.0 (BeOS; U; BeOS BePC; en-US; rv:1.8.1.17) Gecko/20080831 BonEcho/2.0.0.17', 
'Mozilla/5.0 (BeOS; U; BeOS BePC; en-US; rv:1.8.1.6) Gecko/20070731 BonEcho/2.0.0.6', 
'Mozilla/5.0 (BeOS; U; BeOS BePC; en-US; rv:1.8.1.7) Gecko/20070917 BonEcho/2.0.0.7', 
'Mozilla/5.0 (BeOS; U; BeOS BePC; en-US; rv:1.8.1b2) Gecko/20060901 Firefox/2.0b2', 
'Mozilla/5.0 (BeOS; U; BeOS BePC; en-US; rv:1.9a1) Gecko/20051002 Firefox/1.6a1', 
'Mozilla/5.0 (BeOS; U; BeOS BePC; en-US; rv:1.9a1) Gecko/20060702 SeaMonkey/1.5a', 
'Mozilla/5.0 (BeOS; U; Haiku BePC; en-US; rv:1.8.1.10pre) Gecko/20080112 SeaMonkey/1.1.7pre', 
'Mozilla/5.0 (BeOS; U; Haiku BePC; en-US; rv:1.8.1.14) Gecko/20080429 BonEcho/2.0.0.14', 
'Mozilla/5.0 (BeOS; U; Haiku BePC; en-US; rv:1.8.1.17) Gecko/20080831 BonEcho/2.0.0.17', 
'Mozilla/5.0 (Darwin; FreeBSD 5.6; en-GB; rv:1.9.1b3pre)Gecko/20081211 K-Meleon/1.5.2', 
'Mozilla/5.0 (Future Star Technologies Corp.; Star-Blade OS; x86_64; U; en-US) iNet Browser 4.7', 
'Mozilla/5.0 (Linux 2.4.18-18.7.x i686; U) Opera 6.03 [en]', 
'Mozilla/5.0 (Linux 2.4.18-ltsp-1 i686; U) Opera 6.1 [en]', 
'Mozilla/5.0 (Linux 2.4.19-16mdk i686; U) Opera 6.11 [en]', 
'Mozilla/5.0 (Linux 2.4.21-0.13mdk i686; U) Opera 7.11 [en]', 
'Mozilla/5.0 (Linux X86; U; Debian SID; it; rv:1.9.0.1) Gecko/2008070208 Debian IceWeasel/3.0.1', 
'Mozilla/5.0 (Linux i686 ; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.70',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0b8) Gecko/20100101 Firefox/4.0b8',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_7) AppleWebKit/534.24 (KHTML, like Gecko) RockMelt/0.9.56.283', 
'Mozilla/5.0 (compatible; Konqueror/3.1; i686 Linux; 20020811)', 
'Mozilla/5.0 (compatible; Konqueror/3.1; i686 Linux; 20020817)', 
'Mozilla/5.0 (compatible; Konqueror/3.1; i686 Linux; 20020913)', 
'Mozilla/5.0 (compatible; Konqueror/3.1; i686 Linux; 20020928)', 
'Mozilla/5.0 (compatible; Konqueror/3.1; i686 Linux; 20021001)', 
'Mozilla/5.0 (compatible; Konqueror/3.1; i686 Linux; 20021006)', 
'Mozilla/5.0 (compatible; Konqueror/3.1; i686 Linux; 20021007)', 
'Mozilla/5.0 (compatible; Konqueror/3.1; i686 Linux; 20021027)', 
'Mozilla/5.0 (compatible; Konqueror/3.1; i686 Linux; 20021102)', 
'Mozilla/5.0 (compatible; Konqueror/3.1; i686 Linux; 20021103)',
'Mozilla/5.0 (compatible; Konqueror/3.1; i686 Linux; 20021105)', 
'Mozilla/5.0 (compatible; Konqueror/3.1; i686 Linux; 20021106)', 
'Mozilla/5.0 (compatible; Konqueror/3.1; i686 Linux; 20021113)', 
'Mozilla/5.0 (compatible; Konqueror/3.1; i686 Linux; 20021128)', 
'Mozilla/5.0 (compatible; Konqueror/3.2; FreeBSD) (KHTML, like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/3.2; Linux 2.6.2) (KHTML, like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/3.2; Linux) (KHTML, like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/3.2; Linux; X11; en_US) (KHTML, like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/3.3) (KHTML, like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/3.3) KHTML/3.3.2 (like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/3.3; Linux 2.4.22-xfs; X11) KHTML/3.3.2 (like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/3.3; Linux 2.4.27; X11) (KHTML, like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/3.3; Linux 2.6.11) KHTML/3.3.2 (like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/3.3; Linux 2.6.11.12-whnetz-xenU; X11; i686; en_US) KHTML/3.3.2 (like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/3.3; Linux 2.6.11; X11) KHTML/3.3.2 (like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/3.3; Linux 2.6.11; X11; i686) KHTML/3.3.2 (like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/3.3; Linux 2.6.11; X11; i686; de) KHTML/3.3.2 (like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/3.3; Linux 2.6.9-1.667) (KHTML, like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/3.3; Linux) (KHTML, like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/3.3; Linux) KHTML/3.3.2 (like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/3.3; SunOS) (KHTML, like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/3.4) KHTML/3.4.0 (like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/3.4) KHTML/3.4.2 (like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/3.4; Linux 2.6.11; X11)', 
'Mozilla/5.0 (compatible; Konqueror/3.4; Linux 2.6.11; X11) KHTML/3.4.0 (like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/3.4; Linux 2.6.12.6; X11; i686; en_US) KHTML/3.4.3 (like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/3.4; Linux 2.6.12; X11) KHTML/3.4.1 (like Gecko) (Debian package 4:3.4.1-1)', 
'Mozilla/5.0 (compatible; Konqueror/3.4; Linux) KHTML/3.4.0 (like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/3.4; Linux) KHTML/3.4.1 (like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/3.4; Linux) KHTML/3.4.2 (like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/3.4; Linux) KHTML/3.4.2 (like Gecko) (Debian package 4:3.4.2-4)', 
'Mozilla/5.0 (compatible; Konqueror/3.4; Linux) KHTML/3.4.3 (like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/3.4; Linux) KHTML/3.4.3 (like Gecko) (Debian package 4:3.4.3-2)', 
'Mozilla/5.0 (compatible; Konqueror/3.4; Linux) KHTML/3.4.3 (like Gecko) (Kubuntu package 4:3.4.3-0ubuntu1)', 
'Mozilla/5.0 (compatible; Konqueror/3.4; Linux) KHTML/3.4.3 (like Gecko) (Kubuntu package 4:3.4.3-0ubuntu2)', 
'Mozilla/5.0 (compatible; Konqueror/3.4; Linux; de, en_US) KHTML/3.4.2 (like Gecko) (Debian package 4:3.4.2-4)', 
'Mozilla/5.0 (compatible; Konqueror/3.4; SunOS) KHTML/3.4.1 (like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.6 (like Gecko) (Kubuntu)', 
'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.7 (like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.7 (like Gecko) (Debian)', 
'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.7 (like Gecko) (Kubuntu)', 
'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.7 (like Gecko) SUSE', 
'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.9 (like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/3.5; Linux; X11) KHTML/3.5.3 (like Gecko) Kubuntu 6.06 Dapper', 
'Mozilla/5.0 (compatible; Konqueror/3.5; Linux; X11; i686; en_US) KHTML/3.5.6 (like Gecko) (Debian)', 
'Mozilla/5.0 (compatible; Konqueror/3.5; Linux; de) KHTML/3.5.5 (like Gecko) (Debian)',
'Mozilla/5.0 (compatible; Konqueror/3.5; Linux; en_US) KHTML/3.5.6 (like Gecko) (Kubuntu)', 
'Mozilla/5.0 (compatible; Konqueror/3.5; Linux; i686; U; it-IT) KHTML/3.5.5 (like Gecko) (Debian)', 
'Mozilla/5.0 (compatible; Konqueror/3.5; Linux; x86_64) KHTML/3.5.5 (like Gecko)',
'Mozilla/5.0 (compatible; Konqueror/3.5; Linux; x86_64) KHTML/3.5.5 (like Gecko) (Debian)', 
'Mozilla/5.0 (compatible; Konqueror/3.5; Linux; x86_64; en_US) KHTML/3.5.10 (like Gecko) SUSE', 
'Mozilla/5.0 (compatible; Konqueror/3.5; NetBSD 3.0; X11) KHTML/3.5.2 (like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/3.5; NetBSD 4.0_RC3; X11) KHTML/3.5.7 (like Gecko)',
'Mozilla/5.0 (compatible; Konqueror/3.5; SunOS)', 
'Mozilla/5.0 (compatible; Konqueror/3.5; SunOS) KHTML/3.5.0 (like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/3.5; SunOS) KHTML/3.5.1 (like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/3.5; Windows NT 6.0) KHTML/3.5.6 (like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/4.0; Linux) KHTML/4.0.82 (like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/4.0; Linux; x86_64) KHTML/4.0.2 (like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/4.0; Windows) KHTML/4.0.83 (like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/4.0; X11) KHTML/4.0.3 (like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/4.1; DragonFly) KHTML/4.1.4 (like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/4.1; Linux 2.6.27.7-134.fc10.x86_64; X11; x86_64) KHTML/4.1.3 (like Gecko) Fedora/4.1.3-4.fc10', 
'Mozilla/5.0 (compatible; Konqueror/4.1; Linux) KHTML/4.1.3 (like Gecko) Fedora/4.1.3-3.fc10', 
'Mozilla/5.0 (compatible; Konqueror/4.1; Linux) KHTML/4.1.4 (like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/4.1; OpenBSD) KHTML/4.1.4 (like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/4.2) KHTML/4.2.4 (like Gecko) Fedora/4.2.4-2.fc11', 
'Mozilla/5.0 (compatible; Konqueror/4.2; Linux) KHTML/4.2.1 (like Gecko) Fedora/4.2.1-4.fc11', 
'Mozilla/5.0 (compatible; Konqueror/4.2; Linux) KHTML/4.2.2 (like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/4.2; Linux) KHTML/4.2.4 (like Gecko) Fedora/4.2.4-2.fc11', 
'Mozilla/5.0 (compatible; Konqueror/4.2; Linux) KHTML/4.2.4 (like Gecko) Slackware/13.0', 
'Mozilla/5.0 (compatible; Konqueror/4.2; Linux) KHTML/4.2.96 (like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/4.2; Linux) KHTML/4.2.98 (like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/4.2; Linux; X11; x86_64) KHTML/4.2.4 (like Gecko) Fedora/4.2.4-2.fc11', 
'Mozilla/5.0 (compatible; Konqueror/4.3; Linux 2.6.31-16-generic; X11) KHTML/4.3.2 (like Gecko)', 
'Mozilla/5.0 (compatible; Konqueror/4.3; Linux) KHTML/4.3.1 (like Gecko) Fedora/4.3.1-3.fc11', 
'Mozilla/5.0 (compatible; Konqueror/4.4; Linux 2.6.32-22-generic; X11; en_US) KHTML/4.4.3 (like Gecko) Kubuntu', 
'Mozilla/5.0 (compatible; Konqueror/4.4; Linux) KHTML/4.4.1 (like Gecko) Fedora/4.4.1-1.fc12', 
'Mozilla/5.0 (compatible; Konqueror/4.5; FreeBSD) KHTML/4.5.4 (like Gecko)', 
'Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)', 
'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/4.0; InfoPath.2; SV1; .NET CLR 2.0.50727; WOW64)', 
'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)', 
'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)', 
'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', 
'Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0', 
'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1)', 
'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4325)', 
'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)', 
'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; zh-cn) Opera 8.65', 
'Mozilla/5.0 (compatible; MSIE 7.0; Windows 98; SpamBlockerUtility 6.3.91; SpamBlockerUtility 6.2.91; .NET CLR 4.1.89;GB)', 
'Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.0; Trident/4.0; FBSMTWB; .NET CLR 2.0.34861; .NET CLR 3.0.3746.3218; .NET CLR 3.5.33652; msn OptimizedIE8;ENUS)', 
'Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.2; WOW64; .NET CLR 2.0.50727)', 
'Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; c .NET CLR 3.0.04506; .NET CLR 3.5.30707; InfoPath.1; el-GR)', 
'Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 6.0; WOW64; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; c .NET CLR 3.0.04506; .NET CLR 3.5.30707; InfoPath.1; el-GR)',
]
 #
#
#
#
#
#
#

#
#

@app.route("/nasdaqefile", methods =["GET", "POST"])
def nasdaqfile():
    #if request.method == "POST":
    if request.method == "GET":
        if True:
            #url = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=8000"
            url = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=8000&offset=0&?api_key=JNHDh7-LLyDieHsS3zQV"
            #for i in range(1,2):
              #Pick a random user agent
            #  user_agent = random.choice(user_agent_nasdaq)
              #headers = {'User-Agent': user_agent }
            #print(user_agent) 
            #headers = {'User-Agent': ua.random }
            #headers = {'User-Agent': user_agent }
            headers = {'User-Agent' : 'Mozilla/5.0 (compatible; Konqueror/3.1; i686 Linux; 20020811)'}
            r = requests.get(url, headers=headers)
            j = r.json()
            
            table = j['data']['table']
            table_headers = table['headers']

            with open('stocks2.csv', 'w', newline='') as f_output:
              csv_output = csv.DictWriter(f_output, 
              fieldnames=table_headers.values(), extrasaction='ignore')
              csv_output.writeheader()

              for table_row in table['rows']:
                csv_row = {table_headers.get(key, None) : value for key, value in table_row.items()}
                csv_output.writerow(csv_row)
        #html = requests.get(url).content
            print('200')
            # Fill Required Information
            HOSTNAME = "74.208.51.69"
            USERNAME = "stockftpusr"
            PASSWORD = "T11wz8w_"
            #Connect FTP Server
            ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
            #ftp_server.login()
            # force UTF-8 encoding
            ftp_server.encoding = "utf-8"
            #ftp_server.cwd changing required directory
            ftp_server.cwd('/assets/yahoo/yahoo_master/')
            # Enter File Name with Extension
            filename = "stocks2.csv"
            # Read file in binary mode
            with open(filename, "rb") as file:
              # Command for Uploading the file "STOR filename"
              ftp_server.storbinary(f"STOR {filename}", file) 
            # Get list of files
            ftp_server.dir()
            # Close the Connection
            ftp_server.quit()
            #requests.get("https://stocks.desss-portfolio.com/yahoo/most_active")
            requests.get("https://stocks.desss-portfolio.com/yahoo/yahoo_master")
          #losersfile
        return 'ok'
###
###
###
###

@app.route("/nasdaqfile", methods =["GET", "POST"])
def nasdaqfiles():
    #if request.method == "POST":
    if request.method == "GET":
        #if True:
        #url = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=8000&?api_key=JNHDh7-LLyDieHsS3zQV&offset=0"
        url = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=8000&offset=0&?api_key=JNHDh7-LLyDieHsS3zQV"
        for i in range(1,2):
          user_gent = random.choice(user_agent_nasdaq)
          #Pick a random user agent
              #headers = {'User-Agent': user_agent }
          print(user_gent)
            #headers = {'User-Agent': ua.random }
        headers = {'User-Agent': user_gent }
        r = requests.get(url, headers=headers)
        j = r.json()
            
        table = j['data']['table']
        table_headers = table['headers']

        with open('stocks3.csv', 'w', newline='') as f_output:
          csv_output = csv.DictWriter(f_output, 
          fieldnames=table_headers.values(), extrasaction='ignore')
          csv_output.writeheader()

          for table_row in table['rows']:
            csv_row = {table_headers.get(key, None) : value for key, value in table_row.items()}
            csv_output.writerow(csv_row)
        #html = requests.get(url).content
        return 'ok'
  #
#
#
#
###
####
###
###
###
@app.route("/nasdaqcsvfiles", methods =["GET", "POST"])
def nasdaqcsvfile():
    #if request.method == "POST":
    if request.method == "GET":
        if True:
            url = \
    'https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&download=true'
            headers = {'Accept-Language': 'en-US,en;q=0.9',
                       'Accept-Encoding': 'gzip, deflate, br',
                       'User-Agent': 'Java-http-client/'}

            response = requests.get(url, headers=headers)
# get json response
            json = response.json()
# extract relevant keys
            df = pd.DataFrame(json['data']['rows'])
#df
            #df.to_csv('data.csv')
            df.to_csv('stocks2.csv')
        #html = requests.get(url).content
            print('200')
            # Fill Required Information
            HOSTNAME = "74.208.51.69"
            USERNAME = "stockftpusr"
            PASSWORD = "T11wz8w_"
            #Connect FTP Server
            ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
            #ftp_server.login()
            # force UTF-8 encoding
            ftp_server.encoding = "utf-8"
            #ftp_server.cwd changing required directory
            ftp_server.cwd('/assets/yahoo/yahoo_master/')
            # Enter File Name with Extension
            filename = "stocks2.csv"
            # Read file in binary mode
            with open(filename, "rb") as file:
              # Command for Uploading the file "STOR filename"
              ftp_server.storbinary(f"STOR {filename}", file) 
            # Get list of files
            ftp_server.dir()
            # Close the Connection
            ftp_server.quit()
            #requests.get("https://stocks.desss-portfolio.com/yahoo/most_active")
            requests.get("https://stocks.desss-portfolio.com/yahoo/yahoo_master")
          #losersfile
        return 'ok'
###
###
###
###
app.run(host='0.0.0.0', port=8080)