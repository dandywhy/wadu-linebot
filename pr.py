from email import header
from typing import Text
from bs4 import BeautifulSoup
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

import requests 

end_point = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization=CWB-E7F025FB-4BBF-476E-9251-454E9D3FC2E0&limit=1&stationName=string"
data = requests.get(end_point)
earthquake_msg = []
if data.status_code == 500:
    print("無地震資料")
else:
    earthquake_data = data.json()["records"]["earthquake"][0]
    earthquake_msg.append(earthquake_data["reportContent"])
    earthquake_msg.append(earthquake_data["reportImageURI"])
    earthquake_msg.append(earthquake_data["web"])
    earthquake_msg.append(earthquake_data["reportRemark"])
    print(earthquake_msg)