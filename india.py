import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import boto3
import os

aws_access_key_id = os.getenv('AWS_SERVER_PUBLIC_KEY')
aws_secret_access_key = os.getenv('AWS_SERVER_SECRET_KEY')

today = datetime.today().strftime('%Y-%m-%d')

fp = urllib.request.urlopen("https://nvbdcp.gov.in/index4.php?lang=1&level=0&linkid=431&lid=3715")
mybytes = fp.read()
html = mybytes.decode("utf8")
fp.close()
soup = BeautifulSoup(html, features="lxml")
table = soup.find("table")
df = pd.read_html(str(table),header=0)[0]
df = df.dropna()
df.to_csv("india/india_monthly_cases_"+today+".csv", index = False)

s3 = boto3.resource(
    's3', 
    aws_access_key_id=aws_access_key_id, 
    aws_secret_access_key=aws_secret_access_key)

s3.Bucket('tak-insight-priv-dengue-gold').upload_file(
    "india/india_monthly_cases_"+today+".csv", 
    "raw/dengue_cases/india/india_monthly_cases_"+today+".csv")