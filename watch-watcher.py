#!/usr/bin/python
#---------------------------------------------------------------------------#
#                Christopher Stobie <cjstobie@gmail.com>                    #
#---------------------------------------------------------------------------#
import urllib2
import lxml
import boto3
import sys
import os
import logging
import argparse
import texttable as tt
from bs4 import BeautifulSoup

#---------------------------------------------------------------------------#
# Global Vars                                                               #
#---------------------------------------------------------------------------#
# Supported websites: dutyfreeislandshop.com & longislandwatch.com          #
#---------------------------------------------------------------------------#
urls = ["http://www.dutyfreeislandshop.com/citizen-nh8350-83l-automatic-50m-elegant-mens-watch"]

watches = {}
char_count = []
x=[[]]
url_status = 'not_alerted'
home = os.getenv("HOME")
cache_file = '%s/.watch_cache' %home
log_file = '%s/watch-watcher.log' %home
char_count = []
tab = tt.Texttable()
logging.basicConfig(level=logging.INFO, 
    filename = log_file,
    format = '%(asctime)s %(message)s')

#---------------------------------------------------------------------------#
# Ensure our cache file exists                                              #
#---------------------------------------------------------------------------#
try:
    f = open(cache_file)
except IOError:
    f = open(cache_file, 'w+')

#---------------------------------------------------------------------------#
# Get the html data for each URL, and store the stock status in a dict      #
#---------------------------------------------------------------------------#
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

#---------------------------------------------------------------------------#
# Get the character count from each watch product and dynamically set the   #
# column width for our table                                                #
#---------------------------------------------------------------------------#
for key, val in (watches.items()):
    char_count.append(len(key))

longest_product = max(char_count)

#---------------------------------------------------------------------------#
# Set Product Status to alerted or not alerted based on file cache          #
#---------------------------------------------------------------------------#
for key,val in watches.items():
    with open(cache_file) as search:
        for line in search:
            line = line.rstrip()
            if key == line:
                url_status = "already_alerted"

    #---------------------------------------------------------------------------#
    # If product is not alerted, check stock availility and act accordingly     #
    #---------------------------------------------------------------------------#
    if url_status == 'not_alerted':
        if "InStock" in val:
            f = open(cache_file, 'a')
            f.write(key + '\n')
            f.close()
            client = boto3.client('sns')
            print("Publishing availability of %s to SNS\n\n") %key
            response = client.publish(
                TopicArn = "arn:aws:sns:us-west-2:438886243477:Watch-Watcher",
                Message = "Watch %s is available!" %key
            )

    x.append([key, val])

#---------------------------------------------------------------------------#
# Texttable settings                                                        #
#---------------------------------------------------------------------------#
tab.add_rows(x)
tab.set_cols_align(['l', 'l'])
tab.set_cols_width([longest_product, 12])
tab.header(['Product', 'Availability'])

#---------------------------------------------------------------------------#
# Output all watches in urls list and their availability                    #
#---------------------------------------------------------------------------#
logging.info('New Check Starting')
f = open(log_file, 'a')
f.write(tab.draw() + '\n\n')
f.close
