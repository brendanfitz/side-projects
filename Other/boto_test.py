# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 12:01:43 2020

@author: Brendan Non-Admin
"""


import os
import boto3
from aws_config import ACCESS_KEY, SECRET_KEY

s3 = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)


bucket_name = 'metis-projects'
object_name = '^GSPC.csv'
file_name = os.path.join(os.path.expanduser('~'), 'Downloads', '^GSPC.csv')

s3.download_file(bucket_name, object_name, file_name)