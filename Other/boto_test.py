# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 12:01:43 2020

@author: Brendan Non-Admin
"""


import os
import boto3
import os

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')


s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_KEY,
)

bucket_name = 'metis-projects'
object_name = 'pickles/budget_poly_scaler.pkl'
file_name = os.path.join(os.path.expanduser('~'), 'Downloads', 'budget_poly_scaler.pkl')

response = s3.download_file(bucket_name, object_name, file_name)

def aws_download(object_name, filename=None,
    bucket_name='metis-projects',
    bucket_directory='pickles',
    local_directory='metis_app/static/pickles'):

    object_path = bucket_directory + '/' + object_name

    if filename:
        download_path =  local_directory + '/' + filename
    else:
        download_path =  local_directory + '/' + object_name
        
    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_KEY,
    )
    s3.download_file(bucket_name, object_path, download_path)
    
aws_download('luther_model.pkl')