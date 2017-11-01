
import requests
import re
from pprint import pprint
import json

import smtplib
from email.mime.text import MIMEText

class BiggestLosers():

    def __init__(self):
        self.biggestLosers = []
        self.filteredStocks = []

    def getAllStocksData(self):
        y = requests.get('https://finance.yahoo.com/losers')
        ytext = y.text

        logfile1 = open('/Users/vikjava/Personal/hobby_proj/yahoo_finance/logfile1.txt', 'w')
        pprint(ytext, logfile1)
        logfile1.close()

        stockLstr = re.findall(r'YFINANCE:([A-Z,]+)...fallback', ytext)
        print stockLstr
        stockList = stockLstr[0].split(",")
        self.biggestLosers = stockList
        print stockList
        print stockList[0]


    def filterStocks(self):
        if not self.biggestLosers:
            return

        for i in self.biggestLosers:

            d = {}
            #statsUrl = "https://finance.yahoo.com/quote/" + stockList[0] + "/key-statistics?p=" + stockList[0]
            i = i.encode('ascii', 'ignore')
            statsUrl = "http://www.marketwatch.com/investing/stock/" + i
            print statsUrl
            s = requests.get(statsUrl)
            stext = s.text

            if i == "GT":
                print "Printing to logfile 2"
                logfile2 = open('/Users/vikjava/Personal/hobby_proj/yahoo_finance/logfile2.txt', 'w')
                pprint(stext, logfile2)
                logfile2.close()

            pe = re.findall(r'P/E Ratio</small>\n                    <span class="kv__value kv__primary ">([0-9.]+)</span>\n', stext)
            mcap = re.findall(r'Market Cap</small>\n                    <span class="kv__value kv__primary ">\$([0-9.]+B|M)', stext)
            curPrice = re.findall(r'<meta name="price" content="([0-9.]+)">', stext)
            change = re.findall(r'<meta name="priceChangePercent" content="(-[0-9.]+)\%"', stext)
            #div = re.findall(r'Dividend</small>\n                    <span class="kv__value kv__primary ">\$([0-9.]+)</span>', stext)
            #yld = re.findall('Yield</small>\n                    <span class="kv__value kv__primary ">([0-9.]+)%</span>', stext)
            #ranges = re.findall('<mw-rangeBar precision="4" day-open="([0-9.]+)" bar-low="([0-9.]+)"'
            #                    ' bar-high="([0-9.]+)" range-low="([0-9.]+)" range-high="([0-9.]+)"', stext)
            #print pe, mcap, div, yld, ranges[1]

            d[i] = {}
            if not pe or float(pe[0]) > 20.0:
                continue

            d[i]['PE'] = float(pe[0])
            d[i]['curPrice'] = float(curPrice[0])
            d[i]['change'] = float(change[0])
            d[i]['MCAP'] = mcap[0].encode('ascii', 'ignore')
            self.filteredStocks.append(d)
            print d
        pprint(self.filteredStocks)
        l = json.dumps(self.filteredStocks)
        pprint(l)

if __name__ == "__main__":
    bl = BiggestLosers()
    bl.getAllStocksData()
    bl.filterStocks()
    '''
    s= requests.get('http://www.thestreet.com/markets/losers.html')
    stext = s.text
    check2 = re.findall(r'href="/quote/([A-Z]+).html.omorig=market_decliners_[A-Z]+', stext)

    check2 = list(set(check2))

    check3 = (check2 + list(set(check) - set(check2)))

    logfile3 = open('/Users/vikram/programming/personal/yahoo_finance/logfile3.txt', 'w')
    pprint(check3, logfile3)
    logfile3.close()

    # Create a text/plain message
    logfile3 = open('/Users/vikram/programming/personal/yahoo_finance/logfile3.txt', 'r')
    msg = MIMEText(logfile3.read())
    logfile3.close()


    msg['Subject'] = 'The biggest losers of today'
    msg['From'] = 'vikram.g.j.coding@gmail.com'
    msg['To'] = 'vikram.g.j.coding@gmail.com'

    s = smtplib.SMTP('localhost', 1025)
    #s = smtplib.SMTP('localhost')
    s.sendmail('vikram.g.j.coding@gmail.com', 'vikram.g.j.coding@gmail.com', msg.as_string())
    s.quit

    pprint(check3)
'''