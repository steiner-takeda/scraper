import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

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
