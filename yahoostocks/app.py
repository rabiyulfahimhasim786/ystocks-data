#activate_this = '/var/www/flask/a/venv/bin/activate_this.py'

#with open(activate_this) as file_:
#with open(activate_this) as file:
#    exec(file.read(), dict(__file__=activate_this))
from flask import Flask, render_template, request
import bs4
from bs4 import BeautifulSoup
import requests
import random
import csv
import pandas as pd
import time
from datetime import datetime, timedelta

from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
 
#print("now =", now)

# dd/mm/YY H:M:S

dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

app = Flask(__name__)


user_agent_list = [
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174',
 'Mozilla/5.0 (Linux; Android 4.0.4; BNTV600 Build/IMM76L) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.111 Safari/537.36',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B440 Safari/600.1.4',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; yie9; rv:11.0) like Gecko',
 'Mozilla/5.0 (Linux; Android 5.0.2; SM-T530NU Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
 'Mozilla/5.0 (iPad; CPU OS 9_0 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A4325c Safari/601.1',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B466 Safari/600.1.4',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/7.0)',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12D508 Safari/600.1.4',
 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
 'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/44.0.2403.67 Mobile/12H321 Safari/600.1.4',
 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; WOW64; Trident/7.0; .NET4.0E; .NET4.0C)',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
 'Mozilla/5.0 (PlayStation 4 2.57) AppleWebKit/537.73 (KHTML, like Gecko)',
 'Mozilla/5.0 (Windows NT 6.1; rv:31.0) Gecko/20100101 Firefox/31.0',
 'Mozilla/5.0 (Linux; Android 5.0; SM-G900V Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Mobile Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0',
 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 7 Build/LMY48I) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; LCJB; rv:11.0) like Gecko',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:38.0) Gecko/20100101 Firefox/38.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36',
 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0; Touch)',
 'Mozilla/5.0 (Linux; Android 5.0.2; SM-T800 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; MASMJS; rv:11.0) like Gecko',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:39.0) Gecko/20100101 Firefox/39.0',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; TNJB; rv:11.0) like Gecko',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; ASJB; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0.1; SAMSUNG SCH-I545 4G Build/LRX22C) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; EIE10;ENUSMSN; rv:11.0) like Gecko',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.68 Mobile/12H321 Safari/600.1.4',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; MATBJS; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; MASAJS; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 6.1; rv:41.0) Gecko/20100101 Firefox/41.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; MALC; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 AOL/9.7 AOLBuild/4343.4049.US Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/33.0.0.0 Safari/534.24',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; MDDCJS; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:39.0) Gecko/20100101 Firefox/39.0',
 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; yie10; rv:11.0) like Gecko',
 'Mozilla/5.0 (Linux; Android 5.0; SAMSUNG-SM-G900A Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.0.3; en-gb; KFTT Build/IML74K) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36',
 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/8.0)',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; TNJB; rv:11.0) like Gecko',
 'Mozilla/5.0 (X11; CrOS x86_64 7077.111.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.0.4; BNTV400 Build/IMM76L) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.111 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36 LBBROWSER',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0; SAMSUNG SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
 'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.104 AOL/9.8 AOLBuild/4346.18.US Safari/537.36',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; InfoPath.3; GWX:QUALIFIED)',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; MDDCJS; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.104 AOL/9.8 AOLBuild/4346.13.US Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 AOL/9.7 AOLBuild/4343.4043.US Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:23.0) Gecko/20100101 Firefox/23.0',
 'Mozilla/5.0 (Windows NT 5.1; rv:38.0) Gecko/20100101 Firefox/38.0',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.13 Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36',
 'Mozilla/5.0 (iPad; CPU OS 6_0_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A523 Safari/8536.25',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; MANM; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.6.2000 Chrome/30.0.1599.101 Safari/537.36',
 'Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/8.0.57838 Mobile/12H143 Safari/600.1.4',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0',
 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; MDDRJS)',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.22 Safari/537.36',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; MATBJS; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:37.0) Gecko/20100101 Firefox/37.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.104 AOL/9.8 AOLBuild/4346.13.US Safari/537.36',
 'Mozilla/5.0 (Windows NT 5.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
 'Mozilla/5.0 (X11; Linux x86_64; U; en-us) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36',
 'Mozilla/5.0 (X11; CrOS x86_64 6946.86.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.91 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; TNJB; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; MDDRJS; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36',
 'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/8.0.57838 Mobile/12F69 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D201 Safari/9537.53',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; GIL 3.5; rv:11.0) like Gecko',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:41.0) Gecko/20100101 Firefox/41.0',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; LG-V410/V41010d Build/KOT49I.V41010d) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.1599.103 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B411 Safari/600.1.4',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; MATBJS; rv:11.0) like Gecko',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.34 (KHTML, like Gecko) Qt/4.8.1 Safari/534.34',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; USPortal; rv:11.0) like Gecko',
 'Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12H143',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:40.0) Gecko/20100101 Firefox/40.0.2 Waterfox/40.0.2',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; SMJB; rv:11.0) like Gecko',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; CMDTDF; .NET4.0C; .NET4.0E)',
 'Mozilla/5.0 (iPad; CPU OS 6_1_2 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B146 Safari/8536.25',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36',
 'Mozilla/5.0 (MSIE 9.0; Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; TNJB; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0',
 'Mozilla/5.0 (X11; FC Linux i686; rv:24.0) Gecko/20100101 Firefox/24.0',
 'Mozilla/5.0 (X11; CrOS armv7l 7262.52.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.86 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MASAJS; rv:11.0) like Gecko',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; MS-RTC LM 8; .NET4.0C; .NET4.0E)',
 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; yie11; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10532',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; BOIE9;ENUSMSE; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; InfoPath.3)',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; InfoPath.3)',
 'Mozilla/5.0 (Linux; Android 4.4.2; SM-T320 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
 'Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/44.0.2403.67 Mobile/12H143 Safari/600.1.4',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/7.0.55539 Mobile/12H321 Safari/600.1.4',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; 360SE)',
 'Mozilla/5.0 (Linux; Android 5.0.2; LG-V410/V41020c Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/34.0.1847.118 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
 'Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) GSA/7.0.55539 Mobile/11D257 Safari/9537.53',
 'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12F69',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.13 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',
 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)',
 'Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFTHWA Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36',
 'Mozilla/5.0 (Android; Mobile; rv:40.0) Gecko/40.0 Firefox/40.0',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0',
 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 AOL/9.7 AOLBuild/4343.4043.US Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; SM-P600 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; rv:35.0) Gecko/20100101 Firefox/35.0',
 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.22 Safari/537.36',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; 360SE)',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; LCJB; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
 'Mozilla/5.0 (X11; CrOS x86_64 6812.88.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.153 Safari/537.36',
 'Mozilla/5.0 (X11; Linux i686; rv:38.0) Gecko/20100101 Firefox/38.0',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; ASU2JS; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.65 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.13 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/537.16 (KHTML, like Gecko) Version/8.0 Safari/537.16',
 'Mozilla/5.0 (Windows NT 6.1; rv:34.0) Gecko/20100101 Firefox/34.0',
 'Mozilla/5.0 (Linux; Android 5.0; SAMSUNG SM-N900V 4G Build/LRX21V) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.3; KFTHWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/44.1.81 like Chrome/44.0.2403.128 Safari/537.36',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; CMDTDF; .NET4.0C; .NET4.0E; GWX:QUALIFIED)',
 'Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) CriOS/45.0.2454.68 Mobile/11D257 Safari/9537.53',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.6.1000 Chrome/30.0.1599.101 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; GT-P5210 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; MDDSJS; rv:11.0) like Gecko',
 'Mozilla/5.0 (Linux; Android 4.4.2; QTAQZ3 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; QMV7B Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; MATBJS; rv:11.0) like Gecko',
 'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/6.0.51363 Mobile/12H321 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B436 Safari/600.1.4',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/530.19.2 (KHTML, like Gecko) Version/4.0.2 Safari/530.19.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12H321',
 'Mozilla/5.0 (Linux; U; Android 4.0.3; en-ca; KFTT Build/IML74K) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36',
 'Mozilla/5.0 (Windows NT 5.1; rv:30.0) Gecko/20100101 Firefox/30.0',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:40.0) Gecko/20100101 Firefox/40.0.2 Waterfox/40.0.2',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:38.0) Gecko/20100101 Firefox/38.0',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; LCJB; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; NISSC; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9) AppleWebKit/537.71 (KHTML, like Gecko) Version/7.0 Safari/537.71',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; MALC; rv:11.0) like Gecko',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.0.9895 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; MSBrowserIE; rv:11.0) like Gecko',
 'Mozilla/5.0 (Linux; Android 5.0.1; SAMSUNG SM-N910V 4G Build/LRX22C) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.2; rv:40.0) Gecko/20100101 Firefox/40.0',
 'Mozilla/5.0 (Linux; Android 5.0.2; SAMSUNG SM-T530NU Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/3.2 Chrome/38.0.2125.102 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.65 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; LCJB; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 6.0; rv:39.0) Gecko/20100101 Firefox/39.0',
 'Mozilla/5.0 (Linux; Android 5.0.2; SM-T700 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0.1; SAMSUNG-SM-N910A Build/LRX22C) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; ASU2JS; rv:11.0) like Gecko',
 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20120101 Firefox/29.0',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.0.8) Gecko/2009032609 Firefox/3.0.8 (.NET CLR 3.5.30729)',
 'Mozilla/5.0 (X11; CrOS x86_64 7077.95.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.90 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.6.1000 Chrome/30.0.1599.101 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36 LBBROWSER',
 'Mozilla/5.0 (Windows NT 6.1; rv:36.0) Gecko/20100101 Firefox/36.0',
 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36',
 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/7.0)',
 'Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.68 Mobile/12B466 Safari/600.1.4',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; Win64; x64; Trident/6.0; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727)',
 'Mozilla/5.0 (Linux; Android 5.0.2; VK810 4G Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.76.4 (KHTML, like Gecko) Version/7.0.4 Safari/537.76.4',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:40.0) Gecko/20100101 Firefox/40.0',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; SMJB; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; MDDCJS; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; BOIE9;ENUS; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0',
 'Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/6.0.51363 Mobile/12H143 Safari/600.1.4',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:38.0) Gecko/20100101 Firefox/38.0',
 'Mozilla/5.0 (Windows NT 5.1; rv:41.0) Gecko/20100101 Firefox/41.0',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; InfoPath.3)',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2503.0 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.50 (KHTML, like Gecko) Version/9.0 Safari/601.1.50',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; InfoPath.3; GWX:RESERVED)',
 'Mozilla/5.0 (iPad; CPU OS 6_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B141 Safari/8536.25',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Safari/601.1.56',
 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 7 Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
 'Mozilla/5.0 (iPad; CPU OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.68 Mobile/12B440 Safari/600.1.4',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534+ (KHTML, like Gecko) MsnBot-Media /1.0b',
 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/7.0)',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.3; WOW64; Trident/7.0)',
 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G920V Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; ASU2JS; rv:11.0) like Gecko',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 AOL/9.7 AOLBuild/4343.4049.US Safari/537.36',
 'Mozilla/5.0 (X11; CrOS x86_64 6680.78.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.102 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; SM-T520 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.59 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.6.2000 Chrome/30.0.1599.101 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; MAARJS; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; MALNJS; rv:11.0) like Gecko',
 'Mozilla/5.0 (Linux; Android 4.4.2; SM-T900 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
 'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)',
 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36',
 'Mozilla/5.0 (iPad; CPU OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.68 Mobile/12D508 Safari/600.1.4',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:36.0) Gecko/20100101 Firefox/36.0',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2503.0 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.1.2; GT-N8013 Build/JZO54K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFAPWA Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; InfoPath.3)',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:38.0) Gecko/20100101 Firefox/38.0',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MALCJS; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 6.1; rv:30.0) Gecko/20100101 Firefox/30.0',
 'Mozilla/5.0 (Linux; Android 5.0.1; SM-N910V Build/LRX22C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B436 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/7.0.55539 Mobile/12B466 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A405 Safari/600.1.4',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.59 Safari/537.36',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:37.0) Gecko/20100101 Firefox/37.0',
 'Mozilla/5.0 (Linux; Android 4.4.2; SM-T310 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.45 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 10 Build/LMY48I) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; TNJB; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36',
 'Mozilla/5.0 (X11; CrOS x86_64 7077.123.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)',
 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; 360SE)',
 'Mozilla/5.0 (Linux; Android 4.4.2; QMV7A Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B554a Safari/9537.53',
 'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0; SAMSUNG-SM-N900A Build/LRX21V) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.4; XT1080 Build/SU6-7.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; MAARJS; rv:11.0) like Gecko',
 'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/6.0.51363 Mobile/12F69 Safari/600.1.4',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; MALNJS; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.6.2000 Chrome/30.0.1599.101 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; ASJB; rv:11.0) like Gecko',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.73.11 (KHTML, like Gecko) Version/7.0.1 Safari/537.73.11',
 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/7.0; TNJB; 1ButtonTaskbar)',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
 'Mozilla/5.0 (Windows Phone 8.1; ARM; Trident/7.0; Touch; rv:11.0; IEMobile/11.0; NOKIA; Lumia 635) like Gecko',
 'Mozilla/5.0 (iPad; CPU OS 5_0_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A405 Safari/7534.48.3',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:35.0) Gecko/20100101 Firefox/35.0',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; SAMSUNG SM-N910P Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; rv:33.0) Gecko/20100101 Firefox/33.0',
 'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12H321 [Pinterest/iOS]',
 'Mozilla/5.0 (Linux; Android 5.0.1; LGLK430 Build/LRX21Y) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/38.0.2125.102 Safari/537.36',
 'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12H321 Safari',
 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/8.0; 1ButtonTaskbar)',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; NP08; NP08; MAAU; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 5.1; rv:37.0) Gecko/20100101 Firefox/37.0',
 'Mozilla/5.0 (Linux; Android 4.4.2; SM-T217S Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; EIE10;ENUSMSE; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0',
 'Mozilla/5.0 (Windows NT 5.1; rv:35.0) Gecko/20100101 Firefox/35.0',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.76 Safari/537.36',
 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36 LBBROWSER',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; XT1254 Build/SU3TL-39) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.13 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.2; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
 'Mozilla/5.0 (iPad; CPU OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/7.0.55539 Mobile/12B440 Safari/600.1.4',
 'Mozilla/5.0 (MSIE 10.0; Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
 'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/44.0.2403.67 Mobile/12F69 Safari/600.1.4',
 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0.1; SAMSUNG-SGH-I337 Build/LRX22C) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.3; KFASWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/44.1.81 like Chrome/44.0.2403.128 Safari/537.36',
 'Mozilla/5.0 (X11; CrOS armv7l 7077.111.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A403 Safari/8536.25',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0.2; SAMSUNG SM-T800 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/3.0 Chrome/38.0.2125.102 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0; SM-G900V Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.133 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; MAGWJS; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; MALNJS; rv:11.0) like Gecko',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; ATT-IE11; rv:11.0) like Gecko',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.103 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174',
 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7) AppleWebKit/534.48.3 (KHTML, like Gecko) Version/5.1 Safari/534.48.3',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; WOW64; Trident/7.0; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729)',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.13 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/8.0.57838 Mobile/12H321 Safari/600.1.4',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
 'Mozilla/5.0 (iPad; CPU OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/7.0.55539 Mobile/12D508 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D167 Safari/9537.53',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0; MSN 9.0;MSN 9.1;MSN 9.6;MSN 10.0;MSN 10.2;MSN 10.5;MSN 11;MSN 11.5; MSNbMSNI; MSNmen-us; MSNcOTH) like Gecko',
 'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0',
 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.0.9895 Safari/537.36',
 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/7.0; 1ButtonTaskbar)',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.102 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 YaBrowser/15.7.2357.2877 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:27.0) Gecko/20100101 Firefox/27.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; BOIE9;ENUSMSNIP; rv:11.0) like Gecko',
 'Mozilla/5.0 AppleWebKit/999.0 (KHTML, like Gecko) Chrome/99.0 Safari/999.0',
 'Mozilla/5.0 (X11; OpenBSD amd64; rv:28.0) Gecko/20100101 Firefox/28.0',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/538.1 (KHTML, like Gecko) PhantomJS/2.0.0 Safari/538.1',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; MAGWJS; rv:11.0) like Gecko',
 'Mozilla/5.0 (Linux; Android 4.4.2; GT-N5110 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
 'Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.68 Mobile/12B410 Safari/600.1.4',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.7) Gecko/20150824 Firefox/31.9 PaleMoon/25.7.0',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:31.0) Gecko/20100101 Firefox/31.0',
 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:39.0) Gecko/20100101 Firefox/39.0',
 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_0 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A4325c Safari/601.1',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; MS-RTC LM 8; InfoPath.3)',
 'Mozilla/5.0 (Linux; Android 4.4.2; RCT6203W46 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.101 Safari/537.36',
 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:31.0) Gecko/20100101 Firefox/31.0',
 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; Tablet PC 2.0)',
 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; EIE10;ENUSWOL; rv:11.0) like Gecko',
 'Mozilla/5.0 (Linux; Android 4.4.4; en-us; SAMSUNG SM-N910T Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/2.0 Chrome/34.0.1847.76 Mobile Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; RCT6203W46 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.0.4; en-ca; KFJWI Build/IMM76D) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/34.0.1847.116 Chrome/34.0.1847.116 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.22 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.45 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; rv:27.0) Gecko/20100101 Firefox/27.0',
 'Mozilla/5.0 (Linux; Android 4.4.2; RCT6773W22 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; ASJB; ASJB; MAAU; rv:11.0) like Gecko',
 'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B367 Safari/531.21.10',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.7) Gecko/20150824 Firefox/31.9 PaleMoon/25.7.0',
 'Mozilla/5.0 (Linux; Android 5.0; SAMSUNG-SM-G870A Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.3; KFSOWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/44.1.81 like Chrome/44.0.2403.128 Safari/537.36',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; InfoPath.2)',
 'Mozilla/5.0 (Windows NT 5.2; rv:40.0) Gecko/20100101 Firefox/40.0',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.0.9895 Safari/537.36',
 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 AOL/9.7 AOLBuild/4343.4049.US Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; EIE10;ENUSMCM; rv:11.0) like Gecko',
 'Mozilla/5.0 (Linux; Android 5.1.1; SAMSUNG SM-G920P Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/3.2 Chrome/38.0.2125.102 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko)',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:35.0) Gecko/20100101 Firefox/35.0',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; MALCJS; rv:11.0) like Gecko',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36',
 'Mozilla/5.0 (Windows NT 5.2; rv:29.0) Gecko/20100101 Firefox/29.0 /29.0',
 'Mozilla/5.0 (Linux; Android 5.0.2; SM-T550 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 AOL/9.7 AOLBuild/4343.4049.US Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E)',
 'Mozilla/5.0 (Linux; U; Android 4.0.3; en-gb; KFOT Build/IML74K) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0.2; SM-P900 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 9 Build/LMY48I) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; SM-T530NU Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
 'Mozilla/5.0 (X11; Linux i686; rv:40.0) Gecko/20100101 Firefox/40.0',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; SM-T330NU Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.7.1000 Chrome/30.0.1599.101 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:34.0) Gecko/20100101 Firefox/34.0',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.22 Safari/537.36',
 'Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN) AppleWebKit/530.19.2 (KHTML, like Gecko) Version/4.0.2 Safari/530.19.1',
 'Mozilla/5.0 (Android; Tablet; rv:34.0) Gecko/34.0 Firefox/34.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; MALCJS; rv:11.0) like Gecko',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E)',
 'Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) GSA/8.0.57838 Mobile/11D257 Safari/9537.53',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; yie10; rv:11.0) like Gecko',
 'Mozilla/5.0 (Linux; Ubuntu 14.04) AppleWebKit/537.36 Chromium/35.0.1870.2 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; yie11; rv:11.0) like Gecko',]

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
    Rations=[]
 
    for i in range(1,2):
        user_agent = random.choice(user_agent_list)
    print(user_agent) 

    url = "https://finance.yahoo.com/most-active?offset=0&count=100"
    headers = {'User-Agent': user_agent }
    r= requests.get(url, headers=headers)
    data=r.text
    soup=BeautifulSoup(data,'lxml')
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
        for Ration in listing.find_all('td', attrs={'aria-label':'PE Ratio (TTM)'}):
            Rations.append(Ration.text)
 
    dataframe = pd.DataFrame({"Symbols": symbols, "Names": names, "Prices": prices, "Change": changes, "% Change": percentChanges, "Volume": circulatingSupplys, "Average Volume": totalVolumes, "Market Cap": marketCaps, "Ration": Rations, "date/time":dt_string,})#"Volume":circulatingSupplys})
    #dataframe.to_csv('demo.csv')

    dataframe.to_csv('/var/www/flask/a/static/files/mostactive.csv', encoding='utf-8')
    return '200 Status ok'

@app.route('/gainers') 
def gainers():
    ar_=[]
    br_=[]
    cr_=[]
    dr_=[]
    er_=[]
    fr_=[]
    gr_=[]
    hr_=[]
    ir_=[]
 
    for i in range(1,2):
        user_agent = random.choice(user_agent_list)
    print(user_agent) 

    url = "https://finance.yahoo.com/gainers?count=100&offset=0"
    headers = {'User-Agent': user_agent }
    r= requests.get(url, headers=headers)
    data=r.text
    soup=BeautifulSoup(data,'lxml')
    for listing in soup.find_all('tr', attrs={'class':'simpTblRow'}):
        for ar in listing.find_all('td', attrs={'aria-label': 'Symbol'}):
            ar_.append(ar.text)
        for br in listing.find_all('td', attrs={'aria-label':'Name'}):
            br_.append(br.text)
        for cr in listing.find_all('td', attrs={'aria-label':'Price (Intraday)'}):
            cr_.append(cr.text)
        for dr in listing.find_all('td', attrs={'aria-label':'Change'}):
            dr_.append(dr.find('span').text)
        for er in listing.find_all('td', attrs={'aria-label':'% Change'}):
            er_.append(er.find('span').text)
        for fr in listing.find_all('td', attrs={'aria-label':'Avg Vol (3 month)'}):
            fr_.append(fr.text)
        for gr in listing.find_all('td', attrs={'aria-label':'Volume'}):
            gr_.append(gr.text)
        for hr in listing.find_all('td', attrs={'aria-label':'Market Cap'}):
            hr_.append(hr.text)
        for ir in listing.find_all('td', attrs={'aria-label':'PE Ratio (TTM)'}):
            ir_.append(ir.text)
 
    dataframe = pd.DataFrame({"Symbols": ar_, "Names": br_, "Prices": cr_, "Change": dr_, "% Change": er_, "Volume": fr_, "Average Volume": gr_, "Market Cap": hr_, "Ration": ir_, "date/time":dt_string,})#"Volume":circulatingSupplys})
    #dataframe.to_csv('demo.csv')

    dataframe.to_csv('/var/www/flask/a/static/files/gainers.csv', encoding='utf-8')
    return '200 Status ok'

@app.route('/losers') 
def losers():
    ga_=[]
    gb_=[]
    gc_=[]
    gd_=[]
    ge_=[]
    gf_=[]
    gg_=[]
    gh_=[]
    gi_=[]
 
    for i in range(1,2):
        user_agent = random.choice(user_agent_list)
    print(user_agent) 

    url = "https://finance.yahoo.com/losers?count=100&offset=0"
    headers = {'User-Agent': user_agent }
    r= requests.get(url, headers=headers)
    data=r.text
    soup=BeautifulSoup(data,'lxml')
    for listing in soup.find_all('tr', attrs={'class':'simpTblRow'}):
        for ga in listing.find_all('td', attrs={'aria-label': 'Symbol'}):
            ga_.append(ga.text)
        for gb in listing.find_all('td', attrs={'aria-label':'Name'}):
            gb_.append(gb.text)
        for gc in listing.find_all('td', attrs={'aria-label':'Price (Intraday)'}):
            gc_.append(gc.text)
        for gd in listing.find_all('td', attrs={'aria-label':'Change'}):
            gd_.append(gd.find('span').text)
        for ge in listing.find_all('td', attrs={'aria-label':'% Change'}):
            ge_.append(ge.find('span').text)
        for gf in listing.find_all('td', attrs={'aria-label':'Avg Vol (3 month)'}):
            gf_.append(gf.text)
        for gg in listing.find_all('td', attrs={'aria-label':'Volume'}):
            gg_.append(gg.text)
        for gh in listing.find_all('td', attrs={'aria-label':'Market Cap'}):
            gh_.append(gh.text)
        for gi in listing.find_all('td', attrs={'aria-label':'PE Ratio (TTM)'}):
            gi_.append(gi.text)
 
 
    dataframe = pd.DataFrame({"Symbols": ga_, "Names": gb_, "Prices": gc_, "Change": gd_, "% Change": ge_, "Volume": gf_, "Average Volume": gg_, "Market Cap": gh_, "Ration": gi_, "date/time":dt_string,})
    #dataframe.to_csv('demo.csv')

    dataframe.to_csv('/var/www/flask/a/static/files/losers.csv', encoding='utf-8')
    return '200 Status ok'

@app.route('/trendingtickers') 
def trendingtickers():
    sa_=[]
    sb_=[]
    sc_=[]
    sd_=[]
    se_=[]
    sf_=[]
    sg_=[]
    sh_=[]
 
    for i in range(1,2):
        user_agent = random.choice(user_agent_list)
    print(user_agent) 

    url = "https://finance.yahoo.com/trending-tickers"
    headers = {'User-Agent': user_agent }
    r= requests.get(url, headers=headers)
    data=r.text
    soup=BeautifulSoup(data,'lxml')
    for listing in soup.find_all('tr', attrs={'class':'simpTblRow'}):
        for sa in listing.find_all('td', attrs={'aria-label': 'Symbol'}):
            sa_.append(sa.find('a').text)
        for sb in listing.find_all('td', attrs={'aria-label':'Name'}):
            sb_.append(sb.text)
        for sc in listing.find_all('td', attrs={'aria-label':'Last Price'}):
            sc_.append(sc.text)
        for sd in listing.find_all('td', attrs={'aria-label':'Market Time'}):
            sd_.append(sd.text)    
        for se in listing.find_all('td', attrs={'aria-label':'Change'}):
            se_.append(se.find('span').text)
        for sf in listing.find_all('td', attrs={'aria-label':'% Change'}):
            sf_.append(sf.find('span').text)
        for sg in listing.find_all('td', attrs={'aria-label':'Volume'}):
            sg_.append(sg.text)
        for sh in listing.find_all('td', attrs={'aria-label':'Market Cap'}):
            sh_.append(sh.text)

    #dataframe = pd.DataFrame({"Prices": sc_,})
    #print(dataframe)
    dataframe = pd.DataFrame({"Symbols": sa_, "Names": sb_, "Prices": sc_, "Market Time": sd_, "Change": se_, "% Change": sf_, "Volume": sg_, "Market Cap": sh_, "date/time":dt_string,})
    #dataframe.to_csv('demo.csv')

    dataframe.to_csv('/var/www/flask/a/static/files/trendingtickers.csv', encoding='utf-8')
    return '200 Status ok'

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

        with open('/var/www/flask/a/static/files/nasdaqfile.csv', 'w', newline='') as f_output:
          csv_output = csv.DictWriter(f_output, 
          fieldnames=table_headers.values(), extrasaction='ignore')
          csv_output.writeheader()

          for table_row in table['rows']:
            csv_row = {table_headers.get(key, None) : value for key, value in table_row.items()}
            csv_output.writerow(csv_row)
        #html = requests.get(url).content
        return 'ok'

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
            df.to_csv('/var/www/flask/a/static/files/yahoo_nasdaq_current.csv')
            return 'ok'

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
            df.to_csv('/var/www/flask/a/static/files/yahoo_nasdaq_future.csv')
            return 'ok'

if __name__ == '__main__':
    app.run()
