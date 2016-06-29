#!/usr/local/bin/python

from __future__ import print_function
import boto3
import os
import sys

ADMIN_EMAIL = 'xxxxxx@gmail.com'
s3_client = boto3.client('s3')
ses_client = boto3.client('ses', region_name='us-west-2')

def send_email(to, reply, subject, body):
    response = ses_client.send_email(
        Source=ADMIN_EMAIL,
        Destination={
            'ToAddresses': [
                to,
            ]
        },
        Message={
            'Subject': {
                'Data': subject,
            },
            'Body': {
                'Text': {
                    'Data': 'Please download the file from this url.\n'+body,
                },
            }
        },
        ReplyToAddresses=[
            reply,
        ],
        ReturnPath=ADMIN_EMAIL
    )

def send_mail_from_admin(to, message):
    send_email(to, ADMIN_EMAIL, "S3 notification", message)

def lambda_handler(event, context) :
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        print(bucket)
        print(key)
        generated_url=(s3_client.generate_presigned_url(
            ClientMethod = 'get_object',
            Params = {'Bucket' : bucket, 'Key' : key},
            ExpiresIn = 3600,
            HttpMethod = 'GET'))
        send_mail_from_admin('xxxxxx@gmail.com', generated_url)
