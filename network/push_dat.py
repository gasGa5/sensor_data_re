import pandas as pd
from datetime import datetime
import time
import numpy as np
import requests

def post_data(df, url):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=df.to_json(orient='records'), headers=headers)
    return response

def send_data(data):
    post_url = 'http://3.37.201.238/data-upload'

    df = pd.DataFrame(data)
    
    # print(f"{df['time'].iloc[0]} 데이터 추가") 
    response = post_data(df, post_url)
    return response
