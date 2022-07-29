from jinja2 import escape
from flask import Flask, request, redirect, render_template, url_for, jsonify, make_response, flash, redirect,url_for,session,logging,request
import requests
import csv
import random
import yfinance as yf
#import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import json
import optparse
import os
import schedule
import time
from datetime import datetime, timedelta
import ftplib
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
 
#print("now =", now)

# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#print("date and time =", dt_string)
app = Flask('app')
#
#
user_agent_list = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/99.0.1150.36',
'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Vivaldi/4.3',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Vivaldi/4.3',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
#pravin bro -given
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44',
'Mozilla/5.0 (Mobile; LYF/F90M/LYF-F90M-000-02-21-131117; rv:48.0) Gecko/48.0 Firefox/48.0 KAIOS/2.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0 Waterfox/56.2.7',
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.191 Amigo/54.0.2840.191 MRCHROME SOC Safari/537.36',
'Mozilla/5.0 (Linux; Android 8.0; Pixel XL Build/OPP3.170518.006) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.0 Mobile Safari/537.36 EdgA/41.1.35.1',
'Mozilla/5.0 (Linux; Android 5.0.2; SAMSUNG SM-G925F Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36',
  #what is my browser.com
'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)',
'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Mobile/15E148 Safari/604.1',
'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763',
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; KTXN)',
'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16D57',
'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Safari/604.1',
'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
#
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko)',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
'Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Mobile/15E148 Safari/604.1',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Mobile/15E148 Safari/604.1',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko)',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1',
'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1; 125LA; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022)',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
'Mozilla/5.0 (iPhone; CPU iPhone OS 15_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Mobile/15E148 Safari/604.1',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
#
'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)',
'Mozilla/5.0 (Linux; U; Android 2.2) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
'Mozilla/5.0 (iPhone; CPU iPhone OS 14_8_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1',
'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)',
'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
##
#
#github mano given
####
#
#
#
'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36', 
'Mozilla/5.0 (iPad; CPU OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B435 Safari/600.1.4', 
'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240', 
'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; LCJB; rv:11.0) like Gecko',
'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; MDDRJS; rv:11.0) like Gecko',
'Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFAPWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; Touch; rv:11.0) like Gecko',
'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; LCJB; rv:11.0) like Gecko',
'Mozilla/5.0 (Linux; U; Android 4.0.3; en-us; KFOT Build/IML74K) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36',
'Mozilla/5.0 (iPad; CPU OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B329 Safari/8536.25', 
'Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFARWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36', 
'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; ASU2JS; rv:11.0) like Gecko', 
'Mozilla/5.0 (iPad; CPU OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A405 Safari/600.1.4',
'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.77.4 (KHTML, like Gecko) Version/7.0.5 Safari/537.77.4', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36', 
'Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0',
'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; yie11; rv:11.0) like Gecko',
'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MALNJS; rv:11.0) like Gecko', 
'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/8.0.57838 Mobile/12H321 Safari/600.1.4', 
'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
'Mozilla/5.0 (Windows NT 10.0; rv:40.0) Gecko/20100101 Firefox/40.0', 
'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MAGWJS; rv:11.0) like Gecko', 
'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/7.1.5 Safari/537.85.14', 
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; TNJB; rv:11.0) like Gecko', 
'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; NP06; rv:11.0) like Gecko', 
'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36', 
'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:40.0) Gecko/20100101 Firefox/40.0', 
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.4.8 (KHTML, like Gecko) Version/8.0.3 Safari/600.4.8', 
'Mozilla/5.0 (iPad; CPU OS 7_0_6 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B651 Safari/9537.53', 
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.3.18 (KHTML, like Gecko) Version/7.1.3 Safari/537.85.12', 
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko; Google Web Preview) Chrome/27.0.1453 Safari/537.36', 
'Mozilla/5.0 (iPad; CPU OS 8_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A365 Safari/600.1.4', 
'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; rv:39.0) Gecko/20100101 Firefox/39.0', 
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 AOL/9.7 AOLBuild/4343.4049.US Safari/537.36', 
'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36', 
'Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.68 Mobile/12H143 Safari/600.1.4',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:38.0) Gecko/20100101 Firefox/38.0', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:39.0) Gecko/20100101 Firefox/39.0', 
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12H321', 
'Mozilla/5.0 (iPad; CPU OS 7_0_3 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B511 Safari/9537.53', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10', 
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.2.5 (KHTML, like Gecko) Version/7.1.2 Safari/537.85.11', 
'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; ASU2JS; rv:11.0) like Gecko', 
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36',
'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.1) Gecko/2008070208 Firefox/3.0.1', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', 
'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; MDDCJS; rv:11.0) like Gecko', 
'Mozilla/5.0 (Windows NT 6.3; rv:40.0) Gecko/20100101 Firefox/40.0', 
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.34 (KHTML, like Gecko) Qt/4.8.5 Safari/534.34',
'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53 BingPreview/1.0b',
'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0', 
'Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/7.0.55539 Mobile/12H143 Safari/600.1.4', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36', 
'Mozilla/5.0 (X11; CrOS x86_64 7262.52.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.86 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; MDDCJS; rv:11.0) like Gecko', 
'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.4.10 (KHTML, like Gecko) Version/7.1.4 Safari/537.85.13', 
'Mozilla/5.0 (Unknown; Linux x86_64) AppleWebKit/538.1 (KHTML, like Gecko) PhantomJS/2.0.0 Safari/538.1', 
'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; MALNJS; rv:11.0) like Gecko', 
'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.68 Mobile/12F69 Safari/600.1.4',
'Mozilla/5.0 (Android; Tablet; rv:40.0) Gecko/40.0 Firefox/40.0', 
'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.2.5 (KHTML, like Gecko) Version/8.0.2 Safari/600.2.5', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/536.30.1 (KHTML, like Gecko) Version/6.0.5 Safari/536.30.1',
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36', 
'Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFSAWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36', 
'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.104 AOL/9.8 AOLBuild/4346.13.US Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; MAAU; rv:11.0) like Gecko',
'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36',
'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)', 
'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36', 
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.74.9 (KHTML, like Gecko) Version/7.0.2 Safari/537.74.9',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36', 
'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36', 
'Mozilla/5.0 (iPad; CPU OS 7_0_2 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A501 Safari/9537.53',
'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; MAARJS; rv:11.0) like Gecko',
'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36', 
'Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53',
'Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko',
'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/7.0.55539 Mobile/12F69 Safari/600.1.4', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2',
'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0',
'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MASMJS; rv:11.0) like Gecko', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36', 
'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0', 
'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174',
'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; FunWebProducts; rv:11.0) like Gecko', 
'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MAARJS; rv:11.0) like Gecko', 
'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; BOIE9;ENUS; rv:11.0) like Gecko',
'Mozilla/5.0 (Linux; Android 4.4.2; SM-T230NU Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; EIE10;ENUSWOL; rv:11.0) like Gecko',
'Mozilla/5.0 (Windows NT 5.1; rv:39.0) Gecko/20100101 Firefox/39.0', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:39.0) Gecko/20100101 Firefox/39.0',
#
  #
#
#
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
'Mozilla/5.0 (Linux i686; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0b11pre) Gecko/20110126 Firefox/4.0b11pre', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0b8) Gecko/20100101 Firefox/4.0b8', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0) Gecko/20100101 Firefox/9.0', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0a2) Gecko/20111101 Firefox/9.0a2', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.68 Safari/534.24', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/534.31 (KHTML, like Gecko) Chrome/13.0.748.0 Safari/534.31', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.801.0 Safari/535.1', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.803.0 Safari/535.1', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.151 Safari/535.19', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6) AppleWebKit/531.4 (KHTML, like Gecko) Version/4.0.3 Safari/531.4', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_0) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1200.0 Iron/21.0.1200.0 Safari/537.1', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_0) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_3) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.32 Safari/535.1', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_3) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_4) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.100 Safari/534.30', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_4) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.112 Safari/534.30', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_4) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.65 Safari/535.11', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_6) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.12 Safari/534.24', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_6) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.698.0 Safari/534.24', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_6) AppleWebKit/534.24 (KHTML, like Gecko) RockMelt/0.9.56.357 Chrome/11.0.696.71 Safari/534.24', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_6) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.112 Safari/534.30', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_7) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.68 Safari/534.24', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_7) AppleWebKit/534.24 (KHTML, like Gecko) Iron/11.0.700.2 Chrome/11.0.700.2 Safari/534.24', 
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
  #
#
#
####
####
####
####
####
#[
'Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)',
'Mozilla/5.0 (compatible; Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2) Gecko/20070219',
'Mozilla/5.0 (compatible; Windows; U; Windows NT 6.2; WOW64; en-US; rv:12.0) Gecko/20120403211507 Firefox/12.0',
'Mozilla/5.0 (compatible; iCab 3.0.2; Macintosh; U; PPC Mac OS X)',
'Mozilla/5.0 (compatible; iCab 3.0.2; Macintosh; U; PPC Mac OS)',
'Mozilla/5.0 (compatible; iCab 3.0.3; Macintosh; U; PPC Mac OS X)',
'Mozilla/5.0 (compatible; iCab 3.0.3; Macintosh; U; PPC Mac OS)',
'Mozilla/5.0 (compatible; iCab 3.0.5; Macintosh; U; PPC Mac OS X)',
'Mozilla/5.0 (compatible; iCab 3.0.5; Macintosh; U; PPC Mac OS)',
'Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko ) Version/5.1 Mobile/9B176 Safari/7534.48.3',
'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; es-es) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B360 Safari/531.21.10',
'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; es-es) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B367 Safari/531.21.10',
'Mozilla/5.0 (iPad; U; CPU OS 3_2_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B500 Safari/53',
'Mozilla/5.0 (iPad;U;CPU OS 3_2_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B500 Safari/531.21.10',
'Mozilla/5.0 (iPhone Simulator; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7D11 Safari/531.21.10',
'Mozilla/5.0 (iPhone; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_1 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8B117 Safari/6531.22.7',
'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_1 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8B5097d Safari/6531.22.7',
'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; nb-no) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148a Safari/6533.18.5',
'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; ru-ru) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5',
'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3 like Mac OS X; en-gb) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8F190 Safari/6533.18.5',
'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3 like Mac OS X; fr-fr) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8F190 Safari/6533.18.5',
'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3 like Mac OS X; pl-pl) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8F190 Safari/6533.18.5',
'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_1 like Mac OS X; zh-tw) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8G4 Safari/6533.18.5',
'Mozilla/5.0 (iPhone; U; Linux i686; pt-br) AppleWebKit/532+ (KHTML, like Gecko) Version/3.0 Mobile/1A538b Safari/419.3 Midori/0.2.0',
'Mozilla/5.0 (iPhone; U; fr; CPU iPhone OS 4_2_1 like Mac OS X; fr) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148a Safari/6533.18.5',
'Mozilla/5.0 (iPhone; U; ru; CPU iPhone OS 4_2_1 like Mac OS X; fr) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148a Safari/6533.18.5',
'Mozilla/5.0 (iPhone; U; ru; CPU iPhone OS 4_2_1 like Mac OS X; ru) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148a Safari/6533.18.5',
'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_2_1 like Mac OS X; he-il) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5',
'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8G4 Safari/6533.18.5',
'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; ja-jp) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
'Mozilla/5.0 (ipad Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.6 (KHTML, like Gecko) Chrome/7.0.498.0 Safari/534.6',
'Mozilla/5.0 ArchLinux (X11; Linux x86_64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1',
'Mozilla/5.0 ArchLinux (X11; U; Linux x86_64; en-US) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.100',
'Mozilla/5.0 ArchLinux (X11; U; Linux x86_64; en-US) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.100 Safari/534.30',
'Mozilla/5.0 ArchLinux (X11; U; Linux x86_64; en-US) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.60 Safari/534.30',
'Mozilla/5.0 Galeon/1.0.3 (X11; Linux i686; U;) Gecko/0',
'Mozilla/5.0 Galeon/1.2.5 (X11; Linux i586; U;) Gecko/20020623 Debian/1.2.5-0.woody.1',
'Mozilla/5.0 Galeon/1.2.5 (X11; Linux i686; U;) Gecko/0',
'Mozilla/5.0 Galeon/1.2.5 (X11; Linux i686; U;) Gecko/20020610 Debian/1.2.5-1',
'Mozilla/5.0 Galeon/1.2.5 (X11; Linux i686; U;) Gecko/20020623 Debian/1.2.5-0.woody.1',
'Mozilla/5.0 Galeon/1.2.5 (X11; Linux i686; U;) Gecko/20020809',
'Mozilla/5.0 Galeon/1.2.6 (X11; Linux i586; U;) Gecko/20020916',
'Mozilla/5.0 Galeon/1.2.6 (X11; Linux i686; U;) Gecko/20020827',
'Mozilla/5.0 Galeon/1.2.6 (X11; Linux i686; U;) Gecko/20020830',
'Mozilla/5.0 Galeon/1.2.6 (X11; Linux i686; U;) Gecko/20020913 Debian/1.2.6-2',
'Mozilla/5.0 Galeon/1.2.6 (X11; Linux i686; U;) Gecko/20020916',
'Mozilla/5.0 Galeon/1.2.7 (X11; Linux i686; U;) Gecko/20021226 Debian/1.2.7-6',
'Mozilla/5.0 Galeon/1.2.8 (X11; Linux i686; U;) Gecko/20030212',
'Mozilla/5.0 Galeon/1.2.8 (X11; Linux i686; U;) Gecko/20030317',
'Mozilla/5.0 Galeon/1.2.9 (X11; Linux i686; U;) Gecko/20021213 Debian/1.2.9-0.bunk',
'Mozilla/5.0 Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.13) Firefox/3.6.13',
'Mozilla/5.0 Slackware/13.37 (X11; U; Linux x86_64; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/11.0.696.50',
'Mozilla/5.0 Slackware/13.37 (X11; U; Linux x86_64; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/12.0.742.91',
'Mozilla/5.0 Slackware/13.37 (X11; U; Linux x86_64; en-US) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41',
'Mozilla/5.0(Compatible; Windows; U; en-US;) Sundance/0.9',
'Mozilla/5.0(Compatible; Windows; U; en-US;) Sundance/0.9.0.33',
'Mozilla/5.0(Windows; U; Windows NT 5.2; rv:1.9.2) Gecko/20100101 Firefox/3.6',
'Mozilla/5.0(Windows; U; Windows NT 7.0; rv:1.9.2) Gecko/20100101 Firefox/3.6', 'Mozilla/5.0(X11;U;Linux(x86_64);en;rv:1.9a8)Gecko/2007100619;GranParadiso/3.1',
'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/123',
'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10',
'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10gin_lib.cc',
'Mozilla/5.001 (Macintosh; N; PPC; ja) Gecko/25250101',
'Mozilla/5.001 (X11; U; Linux i686; rv:1.8.1.6; de-ch) Gecko/25250101 (ubuntu-feisty)',
'Mozilla/6.0 (Future Star Technologies Corp. Star-Blade OS; U; en-US) iNet Browser 2.5',
'Mozilla/6.0 (Macintosh; I; Intel Mac OS X 11_7_9; de-LI; rv:1.9b4) Gecko/2012010317 Firefox/10.0a4',
'Mozilla/6.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:2.0.0.0) Gecko/20061028 Firefox/3.0',
'Mozilla/6.0 (Windows; U; Windows NT 6.0; en-US) Gecko/2009032609 (KHTML, like Gecko) Chrome/2.0.172.6 Safari/530.7',
'Mozilla/6.0 (Windows; U; Windows NT 6.0; en-US) Gecko/2009032609 Chrome/2.0.172.6 Safari/530.7',
'Mozilla/6.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.8) Gecko/2009032609 Firefox/3.0.8',
'Mozilla/6.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.8) Gecko/2009032609 Firefox/3.0.8 (.NET CLR 3.5.30729)',
'Mozilla/6.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.27 Safari/532.0',
'Mozilla/6.0 (Windows; U; Windows NT 7.0; en-US; rv:1.9.0.8) Gecko/2009032609 Firefox/3.0.9 (.NET CLR 3.5.30729)',
'Mozilla/6.0 (X11; U; Linux x86_64; en-US; rv:2.9.0.3) Gecko/2009022510 FreeBSD/ Sunrise/4.0.1/like Safari',
'Mozilla/5.0 (X11; U; Linux x86_64; en-GB; rv:1.9.0.10) Gecko/2009042523 Ubuntu/9.04 (jaunty) Firefox/3.0.10',
'Mozilla/5.0 (X11; U; Linux x86_64; en-GB; rv:1.9.0.11) Gecko/2009060308 Ubuntu/9.04 (jaunty) Firefox/3.0.11',
'Mozilla/5.0 (X11; U; Linux x86_64; en-GB; rv:1.9.0.11) Gecko/2009061208 Iceweasel/3.0.6 (Debian-3.0.6-1)',
'Mozilla/5.0 (X11; U; Linux x86_64; en-GB; rv:1.9.0.12) Gecko/2009070811 Ubuntu/9.04 (jaunty) Firefox/3.0.12 FirePHP/0.3',
'Mozilla/5.0 (X11; U; Linux x86_64; en-GB; rv:1.9.0.2) Gecko/2008092213 Ubuntu/8.04 (hardy) Firefox/3.0.2',
'Mozilla/5.0 (X11; U; Linux x86_64; en-GB; rv:1.9.0.3) Gecko/2008092510 Ubuntu/8.04 (hardy) Firefox/3.0.3',
'Mozilla/5.0 (X11; U; Linux x86_64; en-GB; rv:1.9.0.5) Gecko/2008122010 Firefox/3.0.5',
'Mozilla/5.0 (X11; U; Linux x86_64; en-GB; rv:1.9.0.7) Gecko/2009030503 Fedora/3.0.7-1.fc9 Firefox/3.0.7',
'Mozilla/5.0 (X11; U; Linux x86_64; en-GB; rv:1.9.0.7) Gecko/2009030719 GranParadiso/3.0.7 FirePHP/0.2.4',
'Mozilla/5.0 (X11; U; Linux x86_64; en-GB; rv:1.9.0.8) Gecko/2009032712 Ubuntu/8.10 (intrepid) Firefox/3.0.8',
'Mozilla/5.0 (X11; U; Linux x86_64; en-GB; rv:1.9.0.8) Gecko/2009032712 Ubuntu/8.10 (intrepid) Firefox/3.0.8 FirePHP/0.2.4',
'Mozilla/5.0 (X11; U; Linux x86_64; en-GB; rv:1.9.0.9) Gecko/2009042113 Ubuntu/8.10 (intrepid) Firefox/3.0.9',
'Mozilla/5.0 (X11; U; Linux x86_64; en-GB; rv:1.9.0.9) Gecko/2009050519 iceweasel/2.0 (Debian-3.0.6-1)',
'Mozilla/5.0 (X11; U; Linux x86_64; en-GB; rv:1.9.2.13) Gecko/20101206 Red Hat/3.6-2.el5 Firefox/3.6.13',
'Mozilla/5.0 (X11; U; Linux x86_64; en-GB; rv:1.9.2.13) Gecko/20101206 Ubuntu/9.10 (karmic) Firefox/3.6.13',
'Mozilla/5.0 (X11; U; Linux x86_64; en-NZ; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.24 Safari/532.0',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.203.0 Safari/532.0',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.203.2 Safari/532.0',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.204.0 Safari/532.0',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.206.0 Safari/532.0',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.207.0 Safari/532.0',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.208.0 Safari/532.0',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.209.0 Safari/532.0',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.211.0 Safari/532.0',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.211.2 Safari/532.0',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.212.0 Safari/532.0',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.213.0 Safari/532.1',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.213.1 Safari/532.1',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.3 Safari/532.1',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.221.3 Safari/532.2',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.221.7 Safari/532.2',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.222.1 Safari/532.2',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.222.4 Safari/532.2',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.222.5 Safari/532.2',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.222.6 Safari/532.2',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.223.2 Safari/532.2',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Comodo_Dragon/4.1.1.11 Chrome/4.1.249.1042 Safari/532.5',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.8 (KHTML, like Gecko) Iron/4.0.275.2 Chrome/4.0.275.2 Safari/532.8',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.308.0 Safari/532.9',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.309.0 Safari/532.9',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/533.1 (KHTML, like Gecko) Chrome/5.0.335.0 Safari/533.1',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/533.2 (KHTML, like Gecko) Chrome/5.0.342.1 Safari/533.2',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/533.2 (KHTML, like Gecko) Chrome/5.0.342.3 Safari/533.2',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/533.3 (KHTML, like Gecko) Arora/0.11.0 Safari/533.3',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/533.3 (KHTML, like Gecko) Chrome/5.0.353.0 Safari/533.3',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/533.3 (KHTML, like Gecko) Chrome/5.0.354.0 Safari/533.3',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/533.3 (KHTML, like Gecko) Chrome/5.0.358.0 Safari/533.3',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.368.0 Safari/533.4',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.375.99 Safari/533.4',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.1 (KHTML, like Gecko) Chrome/6.0.417.0 Safari/534.1',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.1 (KHTML, like Gecko) Chrome/6.0.427.0 Safari/534.1',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/7.0.544.0 Safari/534.10',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.200 Safari/534.10',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.215 Safari/534.10',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Ubuntu/10.10 Chromium/8.0.552.237 Chrome/8.0.552.237 Safari/534.10',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.0 Safari/534.13',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.107 Safari/534.13 v1333515017.9196',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Ubuntu/10.04 Chromium/9.0.595.0 Chrome/9.0.595.0 Safari/534.13',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Ubuntu/10.10 Chromium/9.0.600.0 Chrome/9.0.600.0 Safari/534.14',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.15 (KHTML, like Gecko) Chrome/10.0.613.0 Safari/534.15',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.11 Safari/534.16',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.127 Safari/534.16',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.82 Safari/534.16',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Iron/10.0.650.0 Chrome/10.0.650.0 Safari/534.16',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Iron/10.0.650.1 Chrome/10.0.650.1 Safari/534.16',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Ubuntu/10.10 Chromium/10.0.642.0 Chrome/10.0.642.0 Safari/534.16',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Ubuntu/10.10 Chromium/10.0.648.0 Chrome/10.0.648.0 Safari/534.16',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Ubuntu/10.10 Chromium/10.0.648.127 Chrome/10.0.648.127 Safari/534.16',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Ubuntu/10.10 Chromium/10.0.648.133 Chrome/10.0.648.133 Safari/534.16',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.16 SUSE/10.0.626.0 (KHTML, like Gecko) Chrome/10.0.626.0 Safari/534.16',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.458.1 Safari/534.3',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.470.0 Safari/534.3',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Epiphany/2.30.6 Safari/534.7',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Iron/7.0.520.0 Chrome/7.0.520.0 Safari/534.7',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.20 Safari/535.1',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML, like Gecko) Ubuntu/10.10 Chrome/8.1.0.0 Safari/540.0',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML, like Gecko) Ubuntu/10.10 Chrome/9.1.0.0 Safari/540.0',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML,like Gecko) Chrome/9.1.0.0 Safari/540.0',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) Gecko Firefox/3.0.8',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.7.10) Gecko/20050724 Firefox/1.0.6',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.7.12) Gecko/20050922 Fedora/1.0.7-1.1.fc4 Firefox/1.0.7',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.7.12) Gecko/20051010 Firefox/1.0.7',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.7.12) Gecko/20051010 Firefox/1.0.7 (Ubuntu package 1.0.7)',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.7.12) Gecko/20051127 Firefox/1.0.7',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.7.12) Gecko/20051218 Firefox/1.0.7',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.7.12) Gecko/20060202 CentOS/1.0.7-1.4.3.centos4 Firefox/1.0.7',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.7.6) Gecko/20050405 Firefox/1.0 (Ubuntu package 1.0.2)',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.7.8) Gecko/20050511 Firefox/1.0.4',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.8) Gecko/20051201 Firefox/1.5',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.8) Gecko/20051212 Firefox/1.5',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.8.0.1) Gecko/20060313 Fedora/1.5.0.1-9 Firefox/1.5.0.1 pango-text',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.8.0.10) Gecko/20070409 CentOS/1.5.0.10-2.el5.centos Firefox/1.5.0.10',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.8.0.12) Gecko/20070530 Fedora/1.5.0.12-1.fc6 Firefox/1.5.0.12',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.8.0.12) Gecko/20070718 Red Hat/1.5.0.12-3.el5 Firefox/1.5.0.12',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.8.0.12) Gecko/20080419 CentOS/1.5.0.12-0.15.el4.centos Firefox/1.5.0.12 pango-text'
]
#

#]
#
#
#
#url = 'https://httpbin.org/headers'
#for i in range(1,2):
    #Pick a random user agent
    #user_agent = random.choice(user_agent_list)
    #Set the headers 
    #headers = {'User-Agent': user_agent}
  
@app.route('/')
def hello_world():
  return '<h1>Hello, World!</h1>'
  #for i in range(1,2):
    #Pick a random user agent
    #user_agent = random.choice(user_agent_list)
    #print(user_agent)
  #return '<h1>Hello, World!</h1>'

#app.run(host='0.0.0.0', port=8080)


@app.route('/gainerstables', methods=["GET", "POST"])
def gainerstables():
    # converting csv to html
    data = pd.read_csv('yahoo_gainers1.csv')
    return render_template('gainerstable.html', tables=[data.to_html()], titles=[''])


@app.route('/loserstables', methods=["GET", "POST"])
def loserstables():
    # converting csv to html
    data = pd.read_csv('yahoo_losers1.csv')
    return render_template('loserstable.html', tables=[data.to_html()], titles=[''])

@app.route('/mostactivetables', methods=["GET", "POST"])
def mostactivetables():
    # converting csv to html
    data = pd.read_csv('yahoo_most_active1.csv')
    return render_template('mostactivetable.html', tables=[data.to_html()], titles=[''])

@app.route('/trendingtables', methods=["GET", "POST"])
def trendingtables():
    # converting csv to html
    data = pd.read_csv('yahoo_trending1.csv')
    return render_template('trendingtable.html', tables=[data.to_html()], titles=[''])


@app.route("/gainersfile", methods =["GET", "POST"])
def gainersdatas():
    #if request.method == "POST": # use only for post
    if request.method == "GET":
        if True:
            #url = request.form['text']
            # getting input with name = fname in HTML form
            #ua = pyuser_agent.UA()
            #ua = UserAgent()
            url = 'https://finance.yahoo.com/gainers?offset=0&count=100'
            #url = request.form['namee']
            #gainers = form(name = url)
            #db.session.add(gainers)
            #db.session.commit()
            #url = 'https://finance.yahoo.com/gainers?count=100&offset=0'
            for i in range(1,2):
              #Pick a random user agent
              user_agent = random.choice(user_agent_list)
              #headers = {'User-Agent': user_agent }
            print(user_agent) 
            #headers = {'User-Agent': ua.random } # =use only for post
            headers = {'User-Agent': user_agent }
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
    #df = pd.DataFrame({'Symbol': ac_, 'Name': bc_, 'Price': cc_, 'Change': dc_, 'Change %': ec_, 'Volume': fc_, 'Avg volume': gc_, 'Market cap': hc_, 'Ration': ic_,})
            dict = {'Symbol': ac_, 'Name': bc_, 'Price': cc_, 'Change': dc_, 'Change %': ec_, 'Volume': fc_, 'Avg volume': gc_, 'Market cap': hc_, 'Ration': ic_, 'date/time': dt_string,}
            df = pd.DataFrame(dict)
             # saving the dataframe
            df.to_csv('yahoo_gainers1.csv')
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
            ftp_server.cwd('/assets/yahoo/yahoo_gainers/')
            # Enter File Name with Extension
            filename = "yahoo_gainers1.csv"
            # Read file in binary mode
            with open(filename, "rb") as file:
              # Command for Uploading the file "STOR filename"
              ftp_server.storbinary(f"STOR {filename}", file) 
            # Get list of files
            ftp_server.dir()
            # Close the Connection
            ftp_server.quit()
            requests.get("https://stocks.desss-portfolio.com/yahoo/yahoo_gainers") #schedule.every(10).minutes.until(timedelta(hours=1)).do(gainersdatas)
        #time.sleep(650)
        #requests.get("https://stocks.desss-portfolio.com/yahoo/yahoo_gainers")
            #while 1:
            #  schedule.run_pending()
           #   #time.sleep(1)
           #   if not schedule.jobs:
           #     break
      #time.sleep(1)
        return '200 Status:ok'
        #return 'ok'
    #return render_template("gainersfile.html") use only for post 



@app.route("/gainersdatafile", methods =["GET", "POST"])
def gainersdatafile():
    #if request.method == "POST": # use only for post
    if request.method == "GET":
        if True:
            #url = request.form['text']
            # getting input with name = fname in HTML form
            #ua = pyuser_agent.UA()
            #ua = UserAgent()
            for i in range(1,2):
              #Pick a random user agent
              user_agent = random.choice(user_agent_list)
              #headers = {'User-Agent': user_agent }
            print(user_agent) 
            url = 'https://finance.yahoo.com/gainers?offset=0&count=100'
            #url = request.form['namee']
            #gainers = form(name = url)
            #db.session.add(gainers)
            #db.session.commit()
            #url = 'https://finance.yahoo.com/gainers?count=100&offset=0'
            #headers = {'User-Agent': ua.random } # =use only for post
            headers = {'User-Agent': user_agent }
            html = requests.get(url, headers=headers).content
             #html = requests.get(url).content
            soup = BeautifulSoup(html, 'lxml')
            ab = soup.find_all('a', attrs={'data-test': 'quoteLink'})
            bb = soup.find_all('td', attrs={'aria-label': 'Name'})
            cb = soup.find_all('td', attrs={'aria-label': 'Price (Intraday)'})
            db = soup.find_all('td', attrs={'aria-label': 'Change'})
            eb = soup.find_all('td', attrs={'aria-label': '% Change'})
            fb = soup.find_all('td', attrs={'aria-label': 'Volume'})
            gb = soup.find_all('td', attrs={'aria-label': 'Avg Vol (3 month)'})
            hb = soup.find_all('td', attrs={'aria-label': 'Market Cap'}) 
            ib = soup.find_all('td', attrs={'aria-label': 'PE Ratio (TTM)'})
  

            ab_ = []
            bb_ = []
            cb_ = []
            db_ = []
            eb_ = []
            fb_ = []
            gb_ = []
            hb_ = []
            ib_ = []
            for title in ab:
               ab_.append(title.text.strip())
            for title in bb:
               bb_.append(title.text.strip())
            for title in cb:
              cb_.append(title.text.strip())
            for title in db:
               db_.append(title.text.strip())
            for title in eb:
               eb_.append(title.text.strip())
            for title in fb:
               fb_.append(title.text.strip())
            for title in gb:
              gb_.append(title.text.strip())
            for title in hb:
              hb_.append(title.text.strip())
            for title in ib:
              ib_.append(title.text.strip())
            # dataframe Name and Age columns
    #df = pd.DataFrame({'Symbol': ac_, 'Name': bc_, 'Price': cc_, 'Change': dc_, 'Change %': ec_, 'Volume': fc_, 'Avg volume': gc_, 'Market cap': hc_, 'Ration': ic_,})
            dict = {'Symbol': ab_, 'Name': bb_, 'Price': cb_, 'Change': db_, 'Change %': eb_, 'Volume': fb_, 'Avg volume': gb_, 'Market cap': hb_, 'Ration': ib_,'date/time': dt_string,}
            df = pd.DataFrame(dict)
             # saving the dataframe
            df.to_csv('yahoo_gainers2.csv')
            #url = request.form['namee']
            #gainers = form(name = url)
            #db.session.add(gainers)
            #db.session.commit()
            #url = 'https://finance.yahoo.com/gainers?count=100&offset=0'
            #headers = {'User-Agent': ua.random } # =use only for post
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
            ftp_server.cwd('/assets/yahoo/yahoo_gainers/')
            # Enter File Name with Extension
            filename = "yahoo_gainers2.csv"
            #Read file in binary mode
            with open(filename, "rb") as file:
              # Command for Uploading the file "STOR filename"
              ftp_server.storbinary(f"STOR {filename}", file) 
            # Get list of files
            ftp_server.dir()
            # Close the Connection
            # ftp_server.quit()
            #requests.get("https://stocks.desss-portfolio.com/yahoo/yahoo_gainers") #schedule.every(10).minutes.until(timedelta(hours=1)).do(gainersdatas)
        #time.sleep(650)
        #requests.get("https://stocks.desss-portfolio.com/yahoo/yahoo_gainers")
            #while 1:
            #  schedule.run_pending()
           #   #time.sleep(1)
           #   if not schedule.jobs:
           #     break
      #time.sleep(1)
        return '200 Status:ok'
        #return 'ok'
    #return render_template("gainersfile.html") use only for post 


@app.route("/losersfile", methods =["GET", "POST"])
def losersdatasfile():
    if request.method == "GET":
        if True:
            #url = request.form['text']
            # getting input with name = fname in HTML form
            #ua = pyuser_agent.UA()
            #ua = UserAgent()
            url = 'https://finance.yahoo.com/losers?offset=0&count=100'
            #url = request.form['namee']
            #losers = form(name = url)
            #db.session.add(losers)
            #db.session.commit()
            #url = 'https://finance.yahoo.com/gainers?count=100&offset=0'
            for i in range(1,2):
              #Pick a random user agent
              user_agent = random.choice(user_agent_list)
              #headers = {'User-Agent': user_agent }
            print(user_agent) 
            #headers = {'User-Agent': ua.random }
            headers = {'User-Agent': user_agent }
            html = requests.get(url, headers=headers).content
        #html = requests.get(url).content
            soup = BeautifulSoup(html, 'lxml')
            ar = soup.find_all('a', attrs={'data-test': 'quoteLink'})
            br = soup.find_all('td', attrs={'aria-label': 'Name'})
            cr = soup.find_all('td', attrs={'aria-label': 'Price (Intraday)'})
            dr = soup.find_all('td', attrs={'aria-label': 'Change'})
            er = soup.find_all('td', attrs={'aria-label': '% Change'})
            fr = soup.find_all('td', attrs={'aria-label': 'Volume'})
            gr = soup.find_all('td', attrs={'aria-label': 'Avg Vol (3 month)'})
            hr = soup.find_all('td', attrs={'aria-label': 'Market Cap'})
            ir = soup.find_all('td', attrs={'aria-label': 'PE Ratio (TTM)'})
  

            ar_ = []
            br_ = []
            cr_ = []
            dr_ = []
            er_ = []
            fr_ = []
            gr_ = []
            hr_ = []
            ir_ = []
            for title in ar:
                ar_.append(title.text.strip())
            for title in br:
                br_.append(title.text.strip())
            for title in cr:
                cr_.append(title.text.strip())
            for title in dr:
                dr_.append(title.text.strip())
            for title in er:
                er_.append(title.text.strip())
            for title in fr:
                fr_.append(title.text.strip())
            for title in gr:
                gr_.append(title.text.strip())
            for title in hr:
                hr_.append(title.text.strip())
            for title in ir:
                ir_.append(title.text.strip())
  # dataframe Name and Age columns
            dict = {'Symbol': ar_, 'Name': br_, 'Price': cr_, 'Change': dr_, 'Change %': er_, 'Volume': fr_, 'Avg volume': gr_, 'Market cap': hr_, 'Ration': ir_,'date/time': dt_string,}
            df = pd.DataFrame(dict)
             # saving the dataframe
            df.to_csv('yahoo_losers1.csv')
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
            ftp_server.cwd('/assets/yahoo/yahoo_losers/')
            # Enter File Name with Extension
            filename = "yahoo_losers1.csv"
            # Read file in binary mode
            with open(filename, "rb") as file:
              # Command for Uploading the file "STOR filename"
              ftp_server.storbinary(f"STOR {filename}", file) 
            # Get list of files
            ftp_server.dir()
            # Close the Connection
            ftp_server.quit()
            requests.get("https://stocks.desss-portfolio.com/yahoo/yahoo_losers")
          #losersfile
        return 'ok'
    #return render_template("losersfile.html")
            #df = pd.DataFrame({'Symbol': ar_, 'Name': br_, 'Price': cr_, 'Change': dr_, 'Change %': er_, 'Volume': fr_, 'Avg volume': gr_, 'Market cap': hr_, 'Ration': ir_,})
            #scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/spreadsheets']
           # creds = ServiceAccountCredentials.from_json_keyfile_name('yahoo_losers.json', scope)
            #client = gspread.authorize(creds)
            #spreadsheet_key = '1X7APg9YH6ndu2lEhYDjMrWGwE1mQZlIh3G-XbzV_8zA'
            #wks_name = 'Sheet1'
            #cell_of_start_df = 'A2'
            #d2g.upload(df,
            #spreadsheet_key,
            #wks_name,
            #credentials=creds,
            #col_names=False,
            #row_names=False,
            #start_cell = cell_of_start_df,
            #clean=False)
            #requests.get("https://stocks.desss-portfolio.com/yahoo/yahoo_losers")
          #  return schedule.CancelJob
            
            #return 'ok'
    #schedule.every(1).seconds.do(gainersdatas)
    #while True:
    #    schedule.run_pending()
    #    if not schedule.jobs:
    #        break
    #    time.sleep(1)
    #return render_template("losersfile.html")
    #return make_response(render_template('gainers4.html'),200)
    #else:
       # return render_template("gainers4.html")

#


@app.route("/mostactivefile", methods =["GET", "POST"])
def mostactivefile():
    #if request.method == "POST":
    if request.method == "GET":
        if True:
            #url = request.form['text']
            # getting input with name = fname in HTML form
           # ua = pyuser_agent.UA()
            #ua = UserAgent()
            url = 'https://finance.yahoo.com/most-active?count=100&guce_referrer=aHR0cHM6Ly9sb2dpbi55YWhvby5jb20v&guce_referrer_sig=AQAAAI9gecImEAchRGLbJWaMQRr0edvgHEKjXhV89uZ46DDqOZKQJn7TsZ4k2hHgl09_vQ3_lYa9k_RWrl-tXRFFIR5zhJ5V0CV59JLQKHGfoDQtb_2cD9RLko43tSWYaqR1DtLibvUkwYkJM5MU71P6bpx7nrUwMbOurSz3MmHf7Qey&offset=0'
            #url = request.form['namee']
            #losers = form(name = url)
            #db.session.add(losers)
            #db.session.commit()
            #url = 'https://finance.yahoo.com/gainers?count=100&offset=0'
            for i in range(1,2):
              #Pick a random user agent
              user_agent = random.choice(user_agent_list)
              #headers = {'User-Agent': user_agent }
            print(user_agent) 
            #headers = {'User-Agent': ua.random }
            headers = {'User-Agent': user_agent }
            html = requests.get(url, headers=headers).content
        #html = requests.get(url).content
            soup = BeautifulSoup(html, 'lxml')
            at = soup.find_all('a', attrs={'data-test': 'quoteLink'})
            bt = soup.find_all('td', attrs={'aria-label': 'Name'})
            ct = soup.find_all('td', attrs={'aria-label': 'Price (Intraday)'})
            dt = soup.find_all('td', attrs={'aria-label': 'Change'})
            et = soup.find_all('td', attrs={'aria-label': '% Change'})
            ft = soup.find_all('td', attrs={'aria-label': 'Volume'})
            gt = soup.find_all('td', attrs={'aria-label': 'Avg Vol (3 month)'})
            ht = soup.find_all('td', attrs={'aria-label': 'Market Cap'})
            it = soup.find_all('td', attrs={'aria-label': 'PE Ratio (TTM)'})
  

            at_ = []
            bt_ = []
            ct_ = []
            dt_ = []
            et_ = []
            ft_ = []
            gt_ = []
            ht_ = []
            it_ = []
            for title in at:
                at_.append(title.text.strip())
            for title in bt:
                bt_.append(title.text.strip())
            for title in ct:
                ct_.append(title.text.strip())
            for title in dt:
                dt_.append(title.text.strip())
            for title in et:
                et_.append(title.text.strip())
            for title in ft:
                ft_.append(title.text.strip())
            for title in gt:
                gt_.append(title.text.strip())
            for title in ht:
                ht_.append(title.text.strip())
            for title in it:
                it_.append(title.text.strip())
  # dataframe Name and Age columns

            dict = {'Symbol': at_, 'Name': bt_, 'Price': ct_, 'Change': dt_, 'Change %': et_, 'Volume': ft_, 'Avg volume': gt_, 'Market cap': ht_, 'Ration': it_, 'date/time': dt_string,}
            df = pd.DataFrame(dict)
             # saving the dataframe
            df.to_csv('yahoo_most_active1.csv')
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
            ftp_server.cwd('/assets/yahoo/most_active/')
            # Enter File Name with Extension
            filename = "yahoo_most_active1.csv"
            # Read file in binary mode
            with open(filename, "rb") as file:
              # Command for Uploading the file "STOR filename"
              ftp_server.storbinary(f"STOR {filename}", file) 
            # Get list of files
            ftp_server.dir()
            # Close the Connection
            ftp_server.quit()
            requests.get("https://stocks.desss-portfolio.com/yahoo/most_active")
          #losersfile
        return 'ok'
    #return render_template("mostactivefiles.html")
            #df = pd.DataFrame({'Symbol': at_, 'Name': bt_, 'Price': ct_, 'Change': dt_, 'Change %': et_, 'Volume': ft_, 'Avg volume': gt_, 'Market cap': ht_, 'Ration': it_,})
            #scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/spreadsheets']
            #creds = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scope)
           # client = gspread.authorize(creds)
           # spreadsheet_key = '1hVc3A_XjDt4zYwtEb5YEzQbyyjCn7LcPOQlx03dsHvs'
          #  wks_name = 'Sheet1'
          #  cell_of_start_df = 'A2'
          #  d2g.upload(df,
          #  spreadsheet_key,
          #  wks_name,
         #   credentials=creds,
         #   col_names=False,
         #   row_names=False,
         #   start_cell = cell_of_start_df,
          #  clean=False)
          #  requests.get("https://stocks.desss-portfolio.com/yahoo/most_active")
          #  return schedule.CancelJob
         #   return 'ok'
    #schedule.every(1).seconds.do(gainersdatas)
    #while True:
    #    schedule.run_pending()
    #    if not schedule.jobs:
    #        break
    #    time.sleep(1)
   # return render_template("mostactive4.html")
    #return make_response(render_template('gainers4.html'),200)
    #else:
       # return render_template("gainers4.html")

@app.route("/trendingfile", methods =["GET", "POST"])
def trendingfile():
    #if request.method == "POST":
    if request.method == "GET":
        if True:
            #url = request.form['text']
            # getting input with name = fname in HTML form
            #ua = pyuser_agent.UA()
            #ua = UserAgent()
            url = 'https://finance.yahoo.com/trending-tickers'
            #url = request.form['namee']
            #trending = form(name = url)
            #db.session.add(trending)
            #db.session.commit()
            #url = 'https://finance.yahoo.com/gainers?count=100&offset=0'
            for i in range(1,2):
              #Pick a random user agent
              user_agent = random.choice(user_agent_list)
              #headers = {'User-Agent': user_agent }
            print(user_agent) 
           # headers = {'User-Agent': ua.random }
            headers = {'User-Agent': user_agent }
            html = requests.get(url, headers=headers).content
        #html = requests.get(url).content
            soup = BeautifulSoup(html, 'lxml')

            au = soup.find_all('a', attrs={'class': 'Fw(600) C($linkColor)'})
            bu = soup.find_all('td', attrs={'aria-label': 'Name'})
            cu = soup.find_all('td', attrs={'aria-label': 'Last Price'})
            du = soup.find_all('td', attrs={'aria-label': 'Market Time'})
            eu = soup.find_all('td', attrs={'aria-label': 'Change'})
            fu = soup.find_all('td', attrs={'aria-label': '% Change'})
            gu = soup.find_all('td', attrs={'aria-label': 'Volume'})
            hu = soup.find_all('td', attrs={'aria-label': 'Market Cap'})
  

            au_ = []
            bu_ = []
            cu_ = []
            du_ = []
            eu_ = []
            fu_ = []
            gu_ = []
            hu_ = []
            for title in au:
                au_.append(title.text.strip())
            for title in bu:
                bu_.append(title.text.strip())
            for title in cu:
                cu_.append(title.text.strip())
            for title in du:
                du_.append(title.text.strip())
            for title in eu:
                eu_.append(title.text.strip())
            for title in fu:
                fu_.append(title.text.strip())
            for title in gu:
                gu_.append(title.text.strip())
            for title in hu:
                hu_.append(title.text.strip())
            dict = {'Symbol': au_, 'Name': bu_, 'Price': cu_, 'Market Time': du_, 'Change': eu_, 'Change %': fu_, 'Volume': gu_, 'Market cap': hu_, 'date/time': dt_string,}
            df = pd.DataFrame(dict)
             # saving the dataframe
            df.to_csv('yahoo_trending1.csv')
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
            ftp_server.cwd('/assets/yahoo/yahoo_trending/')
            # Enter File Name with Extension
            filename = "yahoo_trending1.csv"
            # Read file in binary mode
            with open(filename, "rb") as file:
              # Command for Uploading the file "STOR filename"
              ftp_server.storbinary(f"STOR {filename}", file) 
            # Get list of files
            ftp_server.dir()
            # Close the Connection
            ftp_server.quit()
            requests.get("https://stocks.desss-portfolio.com/yahoo/yahoo_trending")
          #losersfile
        return 'ok'
    #return render_template("trendingfiles.html") 
              # dataframe Name and Age columns
           # df = pd.DataFrame({'Symbol': au_, 'Name': bu_, 'Price': cu_, 'Market Time': du_, 'Change': eu_, 'Change %': fu_, 'Volume': gu_, 'Market cap': hu_})
           
          # scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/spreadsheets']
           # creds = ServiceAccountCredentials.from_json_keyfile_name('yahoo_trendings.json', scope)
           # client = gspread.authorize(creds)
            #spreadsheet_key = '1FDbwLYGQHiuVALZBUcId-OggbZxdrO4CJGncd0zoY0Q'
            #wks_name = 'Sheet1'
           # cell_of_start_df = 'A2'
           # d2g.upload(df,
           # spreadsheet_key,
           # wks_name,
           # credentials=creds,
           # col_names=False,
           # row_names=False,
           # start_cell = cell_of_start_df,
           # clean=False)
           # requests.get("https://stocks.desss-portfolio.com/yahoo/yahoo_trending")
          #  return schedule.CancelJob
           # return 'ok'
    #schedule.every(1).seconds.do(gainersdatas)
    #while True:
    #    schedule.run_pending()
    #    if not schedule.jobs:
    #        break
    #    time.sleep(1)
    #return render_template("trending4.html")
    #return make_response(render_template('gainers4.html'),200)
    #else:
       # return render_template("gainers4.html")

#
#
      #

@app.route("/nasdaqc", methods =["GET", "POST"])
def nasdaqc():
    #if request.method == "POST":
    if request.method == "GET":
        if True:
            for i in range(1,2):
                #Pick a random user agent
                user_agent = random.choice(user_agent_list)
            #headers = {'User-Agent': user_agent }
            #print(user_agent)
            url = 'https://finance.yahoo.com/quote/%5EIXIC'

            headers = {'User-Agent': user_agent }
            print(user_agent)
            html = requests.get(url, headers=headers).content
            #html = requests.get(url).content
            soup = BeautifulSoup(html, 'lxml')
            price = soup.find_all('fin-streamer', attrs={'data-test': 'qsp-price'})
            previousclose = soup.find_all('td', attrs={'data-test': 'PREV_CLOSE-value'})
            change = soup.find_all('fin-streamer', attrs={'data-test': 'qsp-price-change'})
            fiftytwo = soup.find_all('td', attrs={'data-test': 'FIFTY_TWO_WK_RANGE-value'})
            day = soup.find_all('td', attrs={'data-test': 'DAYS_RANGE-value'})

            price_ = []
            previousclose_ = []
            change_ = []
            fiftytwo_ = []
            day_ = []

            for title in price:
                price_.append(title.text.strip())
            for title in previousclose:
                previousclose_.append(title.text.strip())
            for title in change:
                change_.append(title.text.strip())
            for title in fiftytwo:
                fiftytwo_.append(title.text.strip())
            for title in day:
                day_.append(title.text.strip())
            #
            dictionary = {'Price': price_, 'Previousclose': previousclose_, 'Change': change_, 'Fiftytwo': fiftytwo_, 'Day': day_, 'date/time': dt_string,} #'Fiftytwo': fiftytwo_, }#'Volume': fb_, 'Avg volume': gb_, 'Market cap': hb_, 'Ration': ib_,}
            df = pd.DataFrame(dictionary)
            # saving the dataframe
            df.to_csv('yahoo_nasdaq_current.csv')
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
            ftp_server.cwd('/assets/yahoo/yahoo_global/')
            # Enter File Name with Extension
            filename = "yahoo_nasdaq_current.csv"
            # Read file in binary mode
            with open(filename, "rb") as file:
              # Command for Uploading the file "STOR filename"
              ftp_server.storbinary(f"STOR {filename}", file) 
            # Get list of files
            ftp_server.dir()
            # Close the Connection
            ftp_server.quit()
            requests.get("https://stocks.desss-portfolio.com/yahoo/yahoo_global_current")
          #losersfile
        return 'ok'
###
      ###
###
####
@app.route("/nasdaqfuture", methods =["GET", "POST"])
def nasdaqfuture():
    #if request.method == "POST":
    if request.method == "GET":
        if True:
            for i in range(1,2):
                #Pick a random user agent
                user_agent = random.choice(user_agent_list)
            #headers = {'User-Agent': user_agent }
            #print(user_agent)
            url = 'https://finance.yahoo.com/quote/NQ%3DF?p=NQ%3DF'
            headers = {'User-Agent': user_agent }
            print(user_agent)
            html = requests.get(url, headers=headers).content
            #html = requests.get(url).content
            soup = BeautifulSoup(html, 'lxml')
            nfutureprice = soup.find_all('fin-streamer', attrs={'data-test': 'qsp-price'})
            changes = soup.find_all('fin-streamer', attrs={'data-test': 'qsp-price-change'})
            lastprice = soup.find_all('td', attrs={'data-test': 'LAST_PRICE-value'})


            futureprice_ = []
            changes_ = []
            lastprice_ = []

            for title in nfutureprice:
                futureprice_.append(title.text.strip())
            for title in changes:
                changes_.append(title.text.strip())
            for title in lastprice:
                lastprice_.append(title.text.strip())
            dictionary = {'Price': futureprice_, 'Change': changes_, 'previous close': lastprice_, 'date/time': dt_string,}
            df = pd.DataFrame(dictionary)
             # saving the dataframe
            df.to_csv('yahoo_nasdaq_future.csv')
            #print(user_agent)
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
            ftp_server.cwd('/assets/yahoo/yahoo_global/')
            # Enter File Name with Extension
            filename = "yahoo_nasdaq_future.csv"
            # Read file in binary mode
            with open(filename, "rb") as file:
              # Command for Uploading the file "STOR filename"
              ftp_server.storbinary(f"STOR {filename}", file) 
            # Get list of files
            ftp_server.dir()
            # Close the Connection
            ftp_server.quit()
            requests.get("https://stocks.desss-portfolio.com/yahoo/yahoo_global_future")
          #losersfile
        return 'ok'
####
      ###
###
      ###
###
      ###
###
###
###
###
###
###
###
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

@app.route("/nasdaqfiles", methods =["GET", "POST"])
def nasdaqfile():
    #if request.method == "POST":
    if request.method == "GET":
        if True:
            url = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=8000"
            for i in range(1,2):
              #Pick a random user agent
              user_agent = random.choice(user_agent_nasdaq)
              #headers = {'User-Agent': user_agent }
            print(user_agent) 
            #headers = {'User-Agent': ua.random }
            headers = {'User-Agent': user_agent }
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
        url = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=8000&offset=0"
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
###
###
###
@app.route('/ystocks301', methods = ['GET', 'POST'])
def ystocks301():
    if(request.method == 'GET'):
      noise_amp=[]         
      #an empty list to store the second column
      with open('No error.csv', 'r') as rf:
        reader = csv.reader(rf, delimiter=',')
        for row in reader:
          noise_amp.append(row[0]) # which row we need to read , 1 is frist row , 2 is second row
        print(noise_amp)
      for i in range(1,2):
          user_gent = random.choice(user_agent_list)
      headers = {'User-Agent': user_gent }
#headers = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)' }
#tikcer  = ['msft','amd','aapl']
      tikcer = noise_amp[0:300]
      print(tikcer)
      dwarfs = []
      for i in range(300):
        dwarfs.append(i)
      print(dwarfs)
      df = pd.DataFrame(index=dwarfs, columns=['symbol', 'regularMarketPrice', 'Change', 'Change Percentage', 'previousClose'])

      for i in range(0,len(tikcer)):
        print(tikcer[i])
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{tikcer[i]}"
        response = requests.get(url, headers=headers)
        print("API is working. status code :" + str(response.status_code))
        datas = json.loads(response.text)
        df.loc[i, 'symbol'] = datas['chart']['result'][0]['meta']['symbol'] or np.nan
        df.loc[i, 'regularMarketPrice'] = datas['chart']['result'][0]['meta']['regularMarketPrice'] or np.nan
        df.loc[i, 'Change'] = round(((datas['chart']['result'][0]['meta']['regularMarketPrice'])-( datas['chart']['result'][0]['meta']['previousClose'])), 2) #or np.nan
        df.loc[i, 'Change Percentage'] = round(((((datas['chart']['result'][0]['meta']['regularMarketPrice'])-( datas['chart']['result'][0]['meta']['previousClose']))/( datas['chart']['result'][0]['meta']['previousClose']))*100), 2) #or np.nan
        df.loc[i, 'previousClose'] = datas['chart']['result'][0]['meta']['previousClose'] or np.nan
      df.to_csv('data300.csv')
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
            
      ftp_server.cwd('/assets/yahoo/yahoo_empty/')
            # Enter File Name with Extension
      filename = "data300.csv"
            # Read file in binary mode
      with open(filename, "rb") as file:
        # Command for Uploading the file "STOR filename"
        ftp_server.storbinary(f"STOR {filename}", file) 
        # Get list of files
      ftp_server.dir()
            # Close the Connection
      ftp_server.quit()
            #requests.get("https://stocks.desss-portfolio.com/yahoo/most_active")
      #requests.get("https://stocks.desss-portfolio.com/yahoo/yahoo_master")
          #losersfile
      return 'ok'
###
###
###
###
###
###
###
###
###
###
@app.route('/ystocks601', methods = ['GET', 'POST'])
def ystocks601():
    if(request.method == 'GET'):
      noise_amp=[]         
      #an empty list to store the second column
      with open('No error.csv', 'r') as rf:
        reader = csv.reader(rf, delimiter=',')
        for row in reader:
          noise_amp.append(row[0]) # which row we need to read , 1 is frist row , 2 is second row
        print(noise_amp)
      for i in range(1,2):
          user_gent = random.choice(user_agent_list)
      headers = {'User-Agent': user_gent }
#headers = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)' }
#tikcer  = ['msft','amd','aapl']
      tikcer = noise_amp[301:601]
      print(tikcer)
      dwarfs = []
      for i in range(300):
        dwarfs.append(i)
      print(dwarfs)
      df = pd.DataFrame(index=dwarfs, columns=['symbol', 'regularMarketPrice', 'Change', 'Change Percentage', 'previousClose'])

      for i in range(0,len(tikcer)):
        print(tikcer[i])
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{tikcer[i]}"
        response = requests.get(url, headers=headers)
        print("API is working. status code :" + str(response.status_code))
        datas = json.loads(response.text)
        df.loc[i, 'symbol'] = datas['chart']['result'][0]['meta']['symbol'] or np.nan
        df.loc[i, 'regularMarketPrice'] = datas['chart']['result'][0]['meta']['regularMarketPrice'] or np.nan
        df.loc[i, 'Change'] = round(((datas['chart']['result'][0]['meta']['regularMarketPrice'])-( datas['chart']['result'][0]['meta']['previousClose'])), 2) #or np.nan
        df.loc[i, 'Change Percentage'] = round(((((datas['chart']['result'][0]['meta']['regularMarketPrice'])-( datas['chart']['result'][0]['meta']['previousClose']))/( datas['chart']['result'][0]['meta']['previousClose']))*100), 2) #or np.nan
        df.loc[i, 'previousClose'] = datas['chart']['result'][0]['meta']['previousClose'] or np.nan
      df.to_csv('data600.csv')
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
            
      ftp_server.cwd('/assets/yahoo/yahoo_empty/')
            # Enter File Name with Extension
      filename = "data600.csv"
            # Read file in binary mode
      with open(filename, "rb") as file:
        # Command for Uploading the file "STOR filename"
        ftp_server.storbinary(f"STOR {filename}", file) 
        # Get list of files
      ftp_server.dir()
            # Close the Connection
      ftp_server.quit()
            #requests.get("https://stocks.desss-portfolio.com/yahoo/most_active")
      #requests.get("https://stocks.desss-portfolio.com/yahoo/yahoo_master")
          #losersfile
      return 'ok'
###
###
###
###
###
###
###
###
@app.route('/ystocks1001', methods = ['GET', 'POST'])
def ystocks1001():
    if(request.method == 'GET'):
      noise_amp=[]         
      #an empty list to store the second column
      with open('No error.csv', 'r') as rf:
        reader = csv.reader(rf, delimiter=',')
        for row in reader:
          noise_amp.append(row[0]) # which row we need to read , 1 is frist row , 2 is second row
        print(noise_amp)
      for i in range(1,2):
          user_gent = random.choice(user_agent_list)
      headers = {'User-Agent': user_gent }
#headers = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)' }
#tikcer  = ['msft','amd','aapl']
      tikcer = noise_amp[602:1002]
      print(tikcer)
      dwarfs = []
      for i in range(400):
        dwarfs.append(i)
      print(dwarfs)
      df = pd.DataFrame(index=dwarfs, columns=['symbol', 'regularMarketPrice', 'Change', 'Change Percentage', 'previousClose'])

      for i in range(0,len(tikcer)):
        print(tikcer[i])
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{tikcer[i]}"
        response = requests.get(url, headers=headers)
        print("API is working. status code :" + str(response.status_code))
        datas = json.loads(response.text)
        df.loc[i, 'symbol'] = datas['chart']['result'][0]['meta']['symbol'] or np.nan
        df.loc[i, 'regularMarketPrice'] = datas['chart']['result'][0]['meta']['regularMarketPrice'] or np.nan
        df.loc[i, 'Change'] = round(((datas['chart']['result'][0]['meta']['regularMarketPrice'])-( datas['chart']['result'][0]['meta']['previousClose'])), 2) #or np.nan
        df.loc[i, 'Change Percentage'] = round(((((datas['chart']['result'][0]['meta']['regularMarketPrice'])-( datas['chart']['result'][0]['meta']['previousClose']))/( datas['chart']['result'][0]['meta']['previousClose']))*100), 2) #or np.nan
        df.loc[i, 'previousClose'] = datas['chart']['result'][0]['meta']['previousClose'] or np.nan
      df.to_csv('data1002.csv')
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
            
      ftp_server.cwd('/assets/yahoo/yahoo_empty/')
            # Enter File Name with Extension
      filename = "data1002.csv"
            # Read file in binary mode
      with open(filename, "rb") as file:
        # Command for Uploading the file "STOR filename"
        ftp_server.storbinary(f"STOR {filename}", file) 
        # Get list of files
      ftp_server.dir()
            # Close the Connection
      ftp_server.quit()
            #requests.get("https://stocks.desss-portfolio.com/yahoo/most_active")
      #requests.get("https://stocks.desss-portfolio.com/yahoo/yahoo_master")
          #losersfile
      return 'ok'
###
###
###
###
app.run(host='0.0.0.0', port=8080)