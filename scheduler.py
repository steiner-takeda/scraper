import schedule
import time
import os 
from datetime import datetime

def job():
    os.system('python3 malaysia.py')
    print("Malaysia extracted at " + str(datetime.now()))
    os.system('python3 srilanka.py')
    print("Srilanka extracted at " + str(datetime.now()))
    os.system('python3 india.py')
    print("India extracted at " + str(datetime.now()))
    os.system('python3 singapore.py')
    print("Singapore extracted at " + str(datetime.now()))


schedule.every().day.at("09:30").do(job)
#schedule.every(10).seconds.do(job)

while 1:
    schedule.run_pending()
    time.sleep(10)