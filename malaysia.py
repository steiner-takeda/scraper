import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import boto3
import os

aws_access_key_id = os.getenv('AWS_SERVER_PUBLIC_KEY')
aws_secret_access_key = os.getenv('AWS_SERVER_SECRET_KEY')

today = datetime.today().strftime('%Y-%m-%d')

fp = urllib.request.urlopen("https://idengue.mysa.gov.my/ide_v3/index.php")
mybytes = fp.read()
html = mybytes.decode("utf8")
fp.close()
soup = BeautifulSoup(html, features="lxml")
table = soup.find("table", attrs={"class":"table table-bordered"})
df = pd.read_html(str(table))[0]
df = df.dropna()
df.to_csv("malaysia/malaysia_daily_cases_"+today+".csv", index = False)

df_final = pd.DataFrame(
    columns=["country","region","year","month","week","day","daily_cases","total_cases","deaths"])

df_final["region"] = df["STATE"]
df_final["country"] = "Malaysia"
df_final["year"] = datetime.today().strftime('%Y')
df_final["month"] = datetime.today().strftime('%m')
df_final["week"] = datetime.today().strftime('%V')
df_final["day"] = datetime.today().strftime('%d')
df_final["daily_cases"] = df.iloc[:, 1]
df_final["total_cases"] = df.iloc[:, 2]

df_saved = pd.read_csv("malaysia/malaysia.csv")
df_saved = df_saved.append(df_final)
df_saved.to_csv("malaysia/malaysia.csv", index = False)

s3 = boto3.resource(
    's3', 
    aws_access_key_id=aws_access_key_id, 
    aws_secret_access_key=aws_secret_access_key)

s3.Bucket('tak-insight-priv-dengue-gold').upload_file(
    "malaysia/malaysia_daily_cases_"+today+".csv", 
    "raw/dengue_cases/malaysia/malaysia_daily_cases_"+today+".csv")

s3.Bucket('tak-insight-priv-dengue-gold').upload_file(
    "malaysia/malaysia.csv", 
    "raw/dengue_cases/malaysia/final/malaysia.csv")
