from enum import unique
from bs4 import BeautifulSoup
import re
from time import gmtime
from traceback import print_tb
from types import prepare_class
from linebot.models import messages
from linebot.models.send_messages import TextSendMessage
from pymongo import IndexModel,ASCENDING,DESCENDING
from random import randint
# from bson.son import SON
import pymongo,pprint,time,requests
# 連線到 MongoDB 雲端資料庫
# client = pymongo.MongoClient("mongodb+srv://root:root1124@waducluster.zsmpm.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
# 把資料放入資料庫中
# db = client.wadubot
# db_web = client.mywebsite

# col_answer = db.answer
# col_rank = db.rank_room
# col_game = db.game_room
# col_test = db_web.test
# index1 = IndexModel([("highest", 1), ("lowest", -1)], name="range")
# index2 = IndexModel([("answer", 1)],name = 'answer')
# db.test.create_indexes([index1, index2])
# col_rank.create_index('point', name = 'rankPOINT')

# result = col_lowest.find_one({'lowest':{'$lt':5}}) 比大小

request_html = requests.get("https://movies.yahoo.com.tw/movie_comingsoon.html",headers={"cookie":"over18=1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"})
request_html.encoding = 'uft-8'
soup = BeautifulSoup(request_html.text, "html.parser")

