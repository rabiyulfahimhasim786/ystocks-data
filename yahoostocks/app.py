from flask import Flask, render_template
import bs4
from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd

app = Flask(__name__)

@app.route('/') 
def hello_world():
   return 'Hello world from Flask!' 


@app.route('/hello') 
def hello():
   return '200 Status ok'

@app.route('/mostactive') 
def mostactive():
    symbols=[]
    names=[]
    prices=[]
    changes=[]
    percentChanges=[]
    marketCaps=[]
    totalVolumes=[]
    circulatingSupplys=[]
 
#for i in range(0,11):
    url = "https://finance.yahoo.com/most-active?offset=0&count=100"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
    r= requests.get(url, headers=headers)
    data=r.text
    soup=BeautifulSoup(data)
    for listing in soup.find_all('tr', attrs={'class':'simpTblRow'}):
        for symbol in listing.find_all('td', attrs={'aria-label': 'Symbol'}):
            symbols.append(symbol.text)
        for name in listing.find_all('td', attrs={'aria-label':'Name'}):
            names.append(name.text)
        for price in listing.find_all('td', attrs={'aria-label':'Price (Intraday)'}):
            prices.append(price.text)
        for change in listing.find_all('td', attrs={'aria-label':'Change'}):
            changes.append(change.find('span').text)
        for percentChange in listing.find_all('td', attrs={'aria-label':'% Change'}):
            percentChanges.append(percentChange.find('span').text)
        for totalVolume in listing.find_all('td', attrs={'aria-label':'Avg Vol (3 month)'}):
            totalVolumes.append(totalVolume.text)
        for circulatingSupply in listing.find_all('td', attrs={'aria-label':'Volume'}):
            circulatingSupplys.append(circulatingSupply.text)
        for marketCap in listing.find_all('td', attrs={'aria-label':'Market Cap'}):
            marketCaps.append(marketCap.text)
 
    dataframe = pd.DataFrame({"Symbols": symbols, "Names": names, "Prices": prices, "Change": changes, "% Change": percentChanges, "Volume": circulatingSupplys, "Average Volume": totalVolumes, "Market Cap": marketCaps,})#"Volume":circulatingSupplys})
    #dataframe.to_csv('demo.csv')

    dataframe.to_csv('./static/files/mostactive.csv', encoding='utf-8')
    return '200 Status ok'


#@app.route('/html') 
#def index():
#   return render_template('index.html')

if __name__ == '__main__':
    app.run()