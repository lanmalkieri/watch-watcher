#!/usr/bin/python
import urllib2
import lxml
import texttable as tt
import boto3
from bs4 import BeautifulSoup
from prettytable import PrettyTable


#---------------------------------------------------------------------------#
# Set whatever URL's you want to monitor here                               #
#---------------------------------------------------------------------------#
urls = ["http://www.dutyfreeislandshop.com/citizen-nh8350-83l-automatic-50m-elegant-mens-watch",
        "http://www.longislandwatch.com/Aeromatic_A1367_Military_Watch_p/a1367.htm"]

watches = {}
char_count = []
x=[[]]

tab = tt.Texttable()

for url in urls:
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, "lxml")
    product = soup.title.string
    stock = soup.findAll(attrs={'itemprop':'availability'})[0].attrs

    if "href" in stock:
        if "OutOfStock" in stock['href']:
            stock_status = "OutOfStock"
        else:
            stock_status = stock['href']
    elif "content" in stock:
        stock_status = stock['content']

    watches[product] = stock_status

char_count = []

for key, val in (watches.items()):
    char_count.append(len(key))

longest_product = max(char_count)

for key,val in watches.items():
    if "InStock" in val:
        print("\nProduct %s is available!\n") %key
    x.append([key, val])

tab.add_rows(x)
tab.set_cols_align(['l', 'l'])
tab.set_cols_width([longest_product, 12])
tab.header(['Product', 'Availability'])

print(tab.draw())
