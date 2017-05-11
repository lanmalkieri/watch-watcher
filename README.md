# Watch Watcher

This script is for watching a list of URL's that point to a watch on one of two websites.
Only these two sites have been tested/supported.

  * dutyfreeislandshop.com 
  * longislandwatch.com


Required Modules:

* beautifulsoup4 4.6.0
* boto3 1.4.4
* botocore 1.5.47
* bs4==0.0.1
* lxml 3.7.3
* texttable 0.8.8

To install all required packages simply run:
```
pip install -r requirements.txt 
```

We utilize AWS SNS for sending emails, so you'll need an AWS account with proper access key permissions to post to SNS. 

Update the url list with the url of whatever watches you want to monitor that are out of stock. Once the watch gets in stock and notifies you it will cache to a file that it notified you and prevent further emails.

For info on how to setup this up in a cron that runs every hour: https://linuxconfig.org/linux-cron-guide
