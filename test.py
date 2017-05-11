#!/usr/bin/python

import boto3

client = boto3.client('sns')
response = client.publish(
    TopicArn = "arn:aws:sns:us-west-2:438886243477:Watch-Watcher",
    Message = "Watch is available"
)

print("Response: %s".format(response))
