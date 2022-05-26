import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

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