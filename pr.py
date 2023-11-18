from email import header
from typing import Text
from bs4 import BeautifulSoup
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

from game import *

import os
import requests 
import pymongo
import random

client = pymongo.MongoClient('mongodb+srv://root:root1124@waducluster.zsmpm.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client.guess_number
col = db.game_room
check = col.find_one({'user_id': 'U6655ddc386a6f27e6338fa5e37f660c'})
if check:
  print('ok')
else:
  print('bad')

# print(col.find_one()['ans'])