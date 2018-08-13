#gets the date, Principal invenstment strategies and Principle investment risks
#from the SECC web site based on "485A" keywords

from urllib.request import urlopen
import csv
from bs4 import BeautifulSoup

date=[]
strat=[]
risk=[]

tweakers=['TIBIX','THOIX','TGVIX','TBWIX','TINGX','THDIX','TVIFX','THIGX','TLDIX','LTUIX','THIIX','TSIIX','TLMIX','LTMIX','THMIX','LTCIX','THNIX','TNYIX','TSSIX','THLSX']


def ticker(symbol): #returns URL of ticker
    print(symbol)
    OPEN=urlopen('https://www.sec.gov/cgi-bin/series?ticker='+symbol+'&CIK=&sc=companyseries&type=N-PX&Find=Search')
    y=OPEN.read().decode("utf-8").split('\n')
    for x in range (0,len(y)):
        if 'hot' in y[x]:
            #print('https://www.sec.gov'+y[x][y[x].find('href')+6:y[x].find('">',y[x].find('href'))])
            return 'https://www.sec.gov'+y[x][y[x].find('href')+6:y[x].find('">',y[x].find('href'))]    

def docu(frase):
    if '.htm' in frase:
        return "https://www.sec.gov"+frase[frase.find('href="')+6:frase.find('.htm')+4]
    elif '.txt' in frase:
        return "https://www.sec.gov"+frase[frase.find('href="')+6:frase.find('.txt')+4]

def nxtfinder(frase):
    temp=frase.find("location='", frase.find("Next 40"))
    return "https://www.sec.gov"+frase[temp+10:frase.find('">',temp)-1]

def decoder(url):
    OPEN=urlopen(url)
    y=OPEN.read().decode("utf-8").split('\n')
    return y

def datef(frase):
    return frase[frase.find('">')+2:frase.find('/div>')-1]

def yumsoup(url):
    OPEN=urlopen(url)
    y=OPEN.read()
    soup = BeautifulSoup(y, "html.parser")    
    return soup.get_text()
    
def main(FIRST):
    print('main')
    for x in range(0,len(FIRST)):
        #print('new line')
        if '485A' in FIRST[x]:
            SEC=decoder(docu(FIRST[x+1]))
            y=0
            while True:
                if 'Filing Date' in SEC[y]:
                    date.append(datef(SEC[y+1]))
                    break
                y=y+1
            
            while True:
                if '/Archives/edgar/data' in SEC[y]:
                    THIRD=yumsoup(docu(SEC[y]))
                    break
                y=y+1

            print ('glf')
            gfl=0
            while True:
                print(gfl)
                gfl=THIRD.lower().find('growth fund', gfl)
                if "investment goal" in str(THIRD[gfl:gfl+40]).lower():
                    PRIN_STRAT=THIRD.find('Principal Investment Strategies', gfl)
                    PRIN_RISK=THIRD.find('Principal Investment Risks', gfl)
                    PAST=THIRD.find('Past Performance of the', gfl)
                    print('dab')
                    strat.append(str(THIRD[PRIN_STRAT:PRIN_RISK]))
                    
                    risk.append(str(THIRD[PRIN_RISK:PAST]))
                    
                    break
                elif gfl==-1:
                    print('Noner')
                    strat.append(str('None'))
                    risk.append(str('None'))
                    break

                elif gfl>(len(THIRD)/2):
                    print('dabpt2')
                    strat.append(str('idk'))
                    risk.append(str('idk'))
                    break

                gfl=gfl+19

    return 0
            


def main_repeater(ree):
    #print(ree)
    FIRST=decoder(ree)

    fpnum=[ree]

    #goes through the pages and looks for 'next 40' to see is there are any more
    #pages after it, if not it stops. It adds the URLs of the various pages onto a
    #list so that they can be later searched for the keyword, '485A' in this case
    x=0
    while True:
        if 'Next 40' in FIRST[x]:
            fpnum.append(nxtfinder(FIRST[x]))
            url_tran=nxtfinder(FIRST[x])
            FIRST=decoder(url_tran)
            x=0
            
        elif x>150:
            break
        x=x+1

    #runs the main fuctions with each of the URLs that got got from the prevoius
    # "while true" block. SEE "def main" above for more details
    #print (len(fpnum))
    #print(fpnum)
    for w in range(0,len(fpnum)):
        print(fpnum[w])
        main(decoder(fpnum[w]))
        #print('one nore')
    


for x in range (0,len(tweakers)-1):
    main_repeater(ticker(tweakers[x]))

#writes it to the csv file
with open('yeetsv.csv', 'w', encoding='utf-8') as csv_file:
    csv_writer =csv.writer(csv_file)

    csv_writer.writerow(date)
    csv_writer.writerow(strat)
    csv_writer.writerow(risk)


        
