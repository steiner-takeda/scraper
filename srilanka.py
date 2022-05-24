import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import boto3
import os

aws_access_key_id = os.getenv('AWS_SERVER_PUBLIC_KEY')
aws_secret_access_key = os.getenv('AWS_SERVER_SECRET_KEY')

today = datetime.today().strftime('%Y-%m-%d')

fp = urllib.request.urlopen("http://www.epid.gov.lk/web/index.php?Itemid=448&lang=en&option=com_casesanddeaths")
mybytes = fp.read()
html = mybytes.decode("utf8")
fp.close()
soup = BeautifulSoup(html, features="lxml")

table = soup.find("table", attrs={"class":"viewDeseasesSumry"})
df = pd.read_html(str(table))[0]
df.columns = ['Month', 'Count']
df = df.dropna()
df.to_csv("scraper/srilanka/srilanka_cases_by_month_"+today+".csv", index = False)

table = soup.find("table", attrs={"class":"viewDeseases"})
df = pd.read_html(str(table))[0]
df = df.dropna()
df.to_csv("scraper/srilanka/srilanka_cases_by_region_"+today+".csv", index = False)

s3 = boto3.resource(
    's3', 
    aws_access_key_id=aws_access_key_id, 
    aws_secret_access_key=aws_secret_access_key)

s3.Bucket('tak-insight-priv-dengue-gold').upload_file(
    'malaysia_daily_cases_2022-05-20.csv', 
    'raw/dengue_cases/malaysia/malaysia_daily_cases_2022-05-21.csv')
