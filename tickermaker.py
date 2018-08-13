from urllib.request import urlopen
import csv
from bs4 import BeautifulSoup

def ticker(symbol): #returns a list 
    OPEN=urlopen('https://www.sec.gov/cgi-bin/series?ticker='+symbol+'&CIK=&sc=companyseries&type=N-PX&Find=Search')
    y=OPEN.read().decode("utf-8").split('\n')
    for x in range (0,len(y)):
        if 'hot' in y[x]:
            return 'https://www.sec.gov'+y[x][y[x].find('href')+6:y[x].find('">',y[x].find('href'))]

print(ticker("TIBIX"))
