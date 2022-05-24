import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

today = datetime.today().strftime('%Y-%m-%d')

fp = urllib.request.urlopen("https://idengue.mysa.gov.my/ide_v3/index.php")
mybytes = fp.read()
html = mybytes.decode("utf8")
fp.close()
soup = BeautifulSoup(html, features="lxml")
table = soup.find("table", attrs={"class":"table table-bordered"})
df = pd.read_html(str(table))[0]
df = df.dropna()
df.to_csv("scraper/malaysia/malaysia_daily_cases_"+today+".csv", index=False)