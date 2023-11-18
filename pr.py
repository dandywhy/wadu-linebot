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

# client = pymongo.MongoClient('mongodb+srv://root:root1124@waducluster.zsmpm.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
# db = client.guess_number
# col = db.game_room

x = '!12353'
y = int(x[1:])
print(y)
# print(col.find_one()['ans'])