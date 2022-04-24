from email import header
from typing import Text
from bs4 import BeautifulSoup
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

import requests 


request_url = requests.get("https://news.campaign.yahoo.com.tw/2019-nCoV/index.php",headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"})
request_url.encoding = 'uft-8'
soup = BeautifulSoup(request_url.text,"html.parser")
time = soup.find("div","sub")
title = soup.find("div","num _big")
titles = soup.find_all("div","num _small")
time_s = time.text
msg = time_s + "\n"
today_stat = title.text
msg += "全台累計確診：" + today_stat + "\n"
other_first = titles[0].text
msg += "本土病例："+ other_first + "\n"
other_second = titles[1].text
msg += "境外移入：" + other_second + "\n"
other_third = titles[2].text
msg += "死亡病例：" + other_third + "\n\n"
msg += "資料來源：衛福部網站"
print(msg)