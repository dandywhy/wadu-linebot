import os
from re import M
from typing import Collection
from bs4.builder import HTMLTreeBuilder
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import *
from linebot.models.responses import UserIds
from pymongo import collection, IndexModel, ASCENDING, DESCENDING
from requests.api import get

# ======這裡是呼叫的檔案內容=====
from message import *
from new import *
from randombot import *
from crawed import *
from game import *
# ======這裡是呼叫的檔案內容=====

# ======python的函數庫==========
import tempfile
import os
import json
import random
import time
import datetime
import pymongo
# ======python的函數庫==========

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(os.environ['ChannelAccessToken'])
# Channel Secret
handler = WebhookHandler(os.environ['ChannelSecret'])
client = pymongo.MongoClient(os.environ['pymongoClient'])

# db for guess_pw
db = client.wadubot
col_rank = db.rank_room
col_answer = db.answer
col_game = db.game_room

# db for guess_number
db_gn = client.guess_number
col_ans = db_gn.answer
col_gr = db_gn.game_room



# 監聽所有來自 /callback 的 Post Request


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

def get_profile(event):
    uid = {}
    user_id = event.source.user_id
    group_id = event.source.group_id
    profile = line_bot_api.get_group_member_profile(group_id, user_id)
    uid = {'name': profile.display_name, 'user_id': profile.user_id}
    return uid

def join_pw(event):
    user = get_profile(event)
    uid = user['user_id']
    nid = user['name']
    rankUID = col_rank.find_one({'user_id': uid})
    col_game.insert_one({'name': nid, 'user_id': uid})
    try:
        if rankUID['user_id'] == uid:
            message = TextSendMessage(text=f'{nid} 已入座!')
    except:
        col_rank.insert_one({'user_id': uid, 'point': 10000})
        message = TextSendMessage(text=f'{nid} 首次入座\n獲得10000點!!')
    return message

def join_nb(event):
    user = get_profile(event)
    uid = user['user_id']
    nid = user['name']
    col_gr.insert_one({'name': nid, 'user_id': uid})
    message = TextSendMessage(text=f'{nid} 已入座!')
    return message

def clear_guessgame():
    col_answer.delete_many({})
    col_game.delete_many({})
    message = TextSendMessage(text='所有玩家已退出\n遊戲已清零!\n要玩先加入遊戲哦~')
    return message

def clear_gg():
    col_ans.delete_many({})
    col_gr.delete_many({})
    message = TextSendMessage(text='所有玩家已退出\n遊戲已清零!\n要玩先加入遊戲哦~')
    return message

def create_answer():
    if col_game.find_one() != None:
        answer = randint(2, 99)
        nid = col_game.find_one()['name']
        if col_answer.find_one() == None:
            col_answer.insert_many([
                {'no': '1', 'answer': answer}, 
                {'no': '2', 'lowest': 1}, 
                {'no': '3', 'highest': 100}, 
                {'no': '4', 'count': 0}
            ])
            number = col_game.estimated_document_count()
            message = TextSendMessage(
                text=f'遊戲開始 ! \n請大家依序輸入\n【 / + 數字 】ex: /87\n範圍 : 1 ~ 100 \n不包含1 和 100\n- - - - - - - - - - - - - - -\n本局玩家 : {number}人\n由 {nid} 先猜')
        else:
            message = TextSendMessage(text='遊戲正在進行哦!')
    else:
        message = TextSendMessage(text='沒人加入怎麼開始拉~')
    return message

def create_answer_nb():
    if col_gr.find_one() != None:
        ans = random.sample(range(1, 10), 4)
        nid = col_gr.find_one()['name']
        if col_ans.find_one() == None:
            col_ans.insert_many([
                {'no': '1', 'ans': ans}, 
                {'no': '2', 'count': 0}
            ])
            number = col_gr.estimated_document_count()
            message = TextSendMessage(
                text=f'遊戲開始 ! \n規則: \n輸入【! + 四位數(數字不重複)】\n ex: !1234，不包含0\n- - - - - - - - - - - - - - -\n本局玩家 : {number}人\n由 {nid} 先猜'
            )
    else:
        message = TextSendMessage(text='沒人餒，先加入吧')    
    return message

def guess_game(guess, nid, count, uid):
    skipNum = col_game.estimated_document_count() - 1
    answer = col_answer.find_one({'no': '1'})['answer']
    lowest = col_answer.find_one({'no': '2'})['lowest']
    highest = col_answer.find_one({'no': '3'})['highest']
    message = []
    if count == skipNum:
        nextName = col_game.find_one()['name']
        if guess < answer and guess > lowest:
            col_answer.find_one_and_update({'no': '4'}, {'$set': {'count': 0}})
            col_answer.find_one_and_update(
                {'no': '2'}, {'$set': {'lowest': guess}})
            message = TextSendMessage(
                text=f'{nid} PASS !\n下一位 : {nextName}\n範圍 : {guess} - {highest}')
        elif guess > answer and guess < highest:
            col_answer.find_one_and_update({'no': '4'}, {'$set': {'count': 0}})
            col_answer.find_one_and_update(
                {'no': '3'}, {'$set': {'highest': guess}})
            message = TextSendMessage(
                text=f'{nid} PASS !\n下一位 : {nextName}\n範圍 : {lowest} - {guess}')
        elif guess <= lowest or guess >= highest:
            message = TextSendMessage(text=f"{nid}\n要打在範圍內哦")
        else:
            col_answer.delete_many({})
            game = col_game.find()
            content = ''
            Flexmessage = json.load(open('continue.json'))
            for doc in game:
                gameUID = doc['user_id']
                gameNID = doc['name']
                if uid == gameUID:
                    losePoint = col_rank.find_one_and_update(
                        {'user_id': uid}, {'$inc': {'point': -500}})
                    content += f'{gameNID}:{losePoint["point"] - 500}點\n'
                else:
                    winPoint = col_rank.find_one_and_update(
                        {'user_id': gameUID}, {'$inc': {'point': 200}})
                    content += f'{gameNID}:{winPoint["point"] + 200}點\n'
            message.append(TextSendMessage(
                text=f'答案 : {answer}\n{nid} BOMB!扣500點\n其餘玩家加200點\n- - - - - - - - - - - - - - -\n剩餘點數 :\n{content}玩累了就打【/離開】'))
            message.append(FlexSendMessage('繼續?', Flexmessage))
    else:
        num = col_answer.find_one({'no': '4'})['count']
        doc = col_game.find().skip(num + 1).limit(1)
        for dic in doc:
            nextName = dic['name']
        if guess < answer and guess > lowest:
            col_answer.find_one_and_update(
                {'no': '4'}, {'$inc': {'count': 1}})['count']
            col_answer.find_one_and_update(
                {'no': '2'}, {'$set': {'lowest': guess}})
            message = TextSendMessage(
                text=f'{nid} PASS !\n下一位 : {nextName}\n範圍 : {guess} - {highest}')
        elif guess > answer and guess < highest:
            col_answer.find_one_and_update(
                {'no': '4'}, {'$inc': {'count': 1}})['count']
            col_answer.find_one_and_update(
                {'no': '3'}, {'$set': {'highest': guess}})
            message = TextSendMessage(
                text=f'{nid} PASS !\n下一位 : {nextName}\n範圍 : {lowest} - {guess}')
        elif guess <= lowest or guess >= highest:
            message = TextSendMessage(text=f"{nid}\n要打在範圍內哦")
        else:
            col_answer.delete_many({})
            game = col_game.find()
            content = ''
            Flexmessage = json.load(open('continue.json'))
            for doc in game:
                gameUID = doc['user_id']
                gameNID = doc['name']
                if uid == gameUID:
                    losePoint = col_rank.find_one_and_update(
                        {'user_id': uid}, {'$inc': {'point': -500}})
                    content += f'{gameNID}:{losePoint["point"] - 500}點\n'
                else:
                    winPoint = col_rank.find_one_and_update(
                        {'user_id': gameUID}, {'$inc': {'point': 200}})
                    content += f'{gameNID}:{winPoint["point"] + 200}點\n'
            message.append(TextSendMessage(
                text=f'答案 : {answer}\n{nid} BOMB!扣500點\n其餘玩家加200點\n- - - - - - - - - - - - - - -\n剩餘點數 :\n{content}玩累了就打【/離開】'))
            message.append(FlexSendMessage('繼續?', Flexmessage))
    return message

def guess_number(guess, nid, count, uid):
    skipNum = col_gr.estimated_document_count() - 1
    ans = col_ans.find_one({'no': '1'})['ans']
    p = 1
    res = 0
    for i in ans:
        i * p
        res += i * p
        p *= 10
    message = []
    if count == skipNum:
        nextName = col_gr.find_one()['name']
        if guess != res:
            a, b = guess_nb(guess, ans)
            col_ans.find_one_and_update({'no': '2'}, {'$set': {'count': 0}})
            message = TextSendMessage(text=f'{nid} {a}A{b}B\n下一位: {nextName}')
        else:
            col_ans.delete_many({})
            message = TextSendMessage(text=f'答案 : {res}\n{nid} 恭喜答對！')
    else:
        n = col_ans.find_one({'no': '2'})['count']
        doc = col_gr.find().skip(num + 1).limit(1)
        for dic in doc:
            nextName = dic['name']
        if guess != res:
            a, b = guess_nb(guess, ans)
            col_ans.find_one_and_update(
                {'no': '2'}, {'$inc': {'count': 1}})['count']
            message = TextSendMessage(text=f'{nid} {a}A{b}B\n下一位: {nextName}')
        else:
            col_ans.delete_many({})
            message = TextSendMessage(text=f'答案 : {res}\n{nid} 恭喜答對！')
    return message
def check_rank(event):
    nid = get_profile(event)['name']
    uid = get_profile(event)['user_id']
    try:
        point = col_rank.find_one({'user_id': uid})['point']
        message = TextSendMessage(text=f'{nid} 目前積分 :\n{point}點')
    except:
        message = TextSendMessage(text=f'{nid} 目前沒有積分\n趕緊加入遊戲吧!')
    return message


@handler.add(JoinEvent)
def handle_join(event):
    newcoming_text = "WADU~WADU~\n請輸入:'指令'\n或輸入:'功能'\n\nWADU~"
    line_bot_api.reply_message(
        event.reply_token, TextMessage(text=newcoming_text))


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text

    if '早' in msg:
        message = TextSendMessage(text=response_wadu())
        line_bot_api.reply_message(event.reply_token, message)
    elif msg == 'Ptt':
        FlexMessage = json.load(open('ptt.json'))
        line_bot_api.reply_message(
            event.reply_token, FlexSendMessage('Ptt', FlexMessage))
    elif msg == '三劍客':
        FlexMessage = json.load(open('bro.json'))
        line_bot_api.reply_message(
            event.reply_token, FlexSendMessage('三劍客', FlexMessage))
    elif msg == '最新電影':
        message = TextSendMessage(text=moive())
        line_bot_api.reply_message(event.reply_token, message)
    elif msg == '收到':
        message = TextSendMessage(text="收到你的收到")
        line_bot_api.reply_message(event.reply_token, message)
    elif msg == '分組':
        FlexMessage = json.load(open('bnb.json'))
        line_bot_api.reply_message(
            event.reply_token, FlexSendMessage('分組', FlexMessage))
    elif msg == '功能':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='🙋‍♂️功能列表🙋‍♂️',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(image_url="https://i.imgur.com/5EUdDxM.png",
                                    action=PostbackAction(
                                        label="PTT", data="1")
                                    ),
                    QuickReplyButton(image_url="https://i.imgur.com/lzIyXLL.png",
                                    action=PostbackAction(
                                        label="終極密碼", data="5")
                                    ),
                    QuickReplyButton(image_url="https://i.imgur.com/8gAY0vH.png",
                                    action=PostbackAction(
                                        label="電影", data="6")
                                    ),
                    QuickReplyButton(image_url="https://i.imgur.com/iLPtvUV.png",
                                    action=PostbackAction(
                                        label="分組", data="7")
                                    )
                ])))
    elif msg == '終極密碼':
        message = []
        FlexMessage = json.load(open('guess_pw.json'))
        message.append(TextSendMessage(text='請先加入遊戲哦!'))
        message.append(FlexSendMessage('終極密碼', FlexMessage))
        line_bot_api.reply_message(event.reply_token, message)
    elif msg == '猜數字':
        message = []
        FlexMessage = json.load(open('guess_nb.json'))
        message.append(TextSendMessage(text='先加入遊戲哦!'))
        message.append(FlexSendMessage('猜數字', FlexMessage))
        line_bot_api.reply_message(event.reply_token, message)
    elif msg == '離開':
        nid = get_profile(event)['name']
        uid = get_profile(event)['user_id']
        col_game.delete_one({'name': nid, 'user_id': uid})
        message = TextSendMessage(text=f'{nid} 離開遊戲囉!')
        line_bot_api.reply_message(event.reply_token, message)
    elif msg == '解散':
        message = clear_guessgame()
        line_bot_api.reply_message(event.reply_token, message)
    elif msg == 'Wadu離開':
        roomId = event.source.room_id
        try:
            line_bot_api.leave_room(roomId)
        except LineBotApiError as e:
            print('leave error')
    elif msg == 'Wadu滾':
        groupId = event.source.group_id
        try:
            line_bot_api.leave_group(groupId)
        except LineBotApiError as e:
            print('leave error')
    elif msg == '積分':
        message = check_rank(event)
        line_bot_api.reply_message(event.reply_token, message)
    elif msg == '/disbank':
        col_rank.delete_many({})
        message = TextSendMessage(text='資料已清空!')
        line_bot_api.reply_message(event.reply_token, message)
    elif msg == '私聊':
        FlexMessage = json.load(open('minichat.json'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('minichat',FlexMessage))
    if msg[2:4] == "天氣":
        station = msg[:2]
        WeatherMsg = MakeWeather(station)
        if not WeatherMsg:
            WeatherMsg = "查無此測站天氣狀況"
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=WeatherMsg))
    if msg[2:4] == "空氣":
        location = msg[:2]
        AirMsg = MakeAQI(location)
        if not AirMsg:
            AirMsg = "查無此測站空氣品質"
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=AirMsg))
    if msg == '指令':
        message = "目前指令:\n功能\n分組\nPtt\n最新電影\n疫情\n地區測站+天氣(ex:福山天氣)\n地區測站+空氣(ex:淡水空氣)"
        line_bot_api.reply_message(
            event.reply_token, TextMessage(text=message))
    if msg[0] == '!':
        guess = int(msg[1:5])
        nid = get_profile(event)['name']
        uid = get_profile(event)['user_id']
        count = col_ans.find_one({'no': '2'})['count']
        gameUID = col_gr.find_one({'user_id': uid})['user_id']
        res = col_gr.find().skip(count).limit(1)
        for doc in res:
            nowUID = doc['user_id']
            if gameUID == nowUID:
                if isinstance(guess, int) == True:
                    message = guess_number(guess, nid, count, uid)
                    line_bot_api.reply_message(event.reply_token, message)

    if msg[0] == '/':
        guess = int(msg[1:3])
        nid = get_profile(event)['name']
        uid = get_profile(event)['user_id']
        count = col_answer.find_one({'no': '4'})['count']
        gameUID = col_game.find_one({'user_id': uid})['user_id']
        result = col_game.find().skip(count).limit(1)
        for doc in result:
            nowUID = doc['user_id']
            if gameUID == nowUID:
                if isinstance(guess, int) == True:
                    message = guess_game(guess, nid, count, uid)
                    line_bot_api.reply_message(event.reply_token, message)


# PostbackEvent
@handler.add(PostbackEvent)
def handle_message(event):
    data = event.postback.data
    user_id = event.source.user_id
    group_id = event.source.group_id
    profile = line_bot_api.get_group_member_profile(group_id, user_id)
    name = profile.display_name
    uid = profile.user_id

    if data == '1':
        FlexMessage = json.load(open('ptt.json'))
        line_bot_api.reply_message(
            event.reply_token, FlexSendMessage('Ptt', FlexMessage))
    elif data == '2':
        message = TextSendMessage(text=name + "已分組：" + random_bot2v())
        line_bot_api.reply_message(event.reply_token, message)
    elif data == '3':
        message = TextSendMessage(text=name + "已分組：" + random_bot3v())
        line_bot_api.reply_message(event.reply_token, message)
    elif data == '4':
        message = TextSendMessage(text=name + "已分組：" + random_bot4v())
        line_bot_api.reply_message(event.reply_token, message)
    elif data == '5':
        message = []
        FlexMessage = json.load(open('guess_pw.json'))
        message.append(TextSendMessage(text='請先加入遊戲哦!'))
        message.append(FlexSendMessage('終極密碼', FlexMessage))
        line_bot_api.reply_message(event.reply_token,  message)
    elif data == '6':
        message = TextSendMessage(text=moive())
        line_bot_api.reply_message(event.reply_token, message)
    elif data == '7':
        FlexMessage = json.load(open('bnb.json'))
        line_bot_api.reply_message(
            event.reply_token, FlexSendMessage('分組', FlexMessage))
    elif data == '8':
        message = TextSendMessage(text=name + "哈囉\n" + gossiping_ptt())
        line_bot_api.reply_message(event.reply_token, message)
    elif data == '9':
        message = TextSendMessage(text=name + "哈囉\n" + beauty_ptt())
        line_bot_api.reply_message(event.reply_token, message)
    elif data == '10':
        message = TextSendMessage(text=name + "哈囉\n" + moive_ptt())
        line_bot_api.reply_message(event.reply_token, message)
    elif data == '11':
        message = TextSendMessage(text=name + "哈囉\n" + stock_ptt())
        line_bot_api.reply_message(event.reply_token, message)
    elif data == 'clear':
        col_rank.delete_many({})
        message = TextSendMessage(text="紀錄已清除")
        line_bot_api.reply_message(event.reply_token, message)
    elif data == 'check':
        message = check_rank(event)
        line_bot_api.reply_message(event.reply_token, message)
    elif data == 'joingame':
        message = join_pw(event)
        line_bot_api.reply_message(event.reply_token, message)
    elif data == 'joingame_nb':
        message = join_nb(event)
        line_bot_api.reply_message(event.reply_token, message)
    elif data == 'start':
        if col_game.estimated_document_count() > 1:
            message = create_answer()
            line_bot_api.reply_message(event.reply_token, message)
        else:
            message = TextSendMessage(text='至少兩人才能玩哦')
            line_bot_api.reply_message(event.reply_token, message)
    elif data == 'start_nb':
        if col_game.estimated_document_count() == 3:
            message = TextSendMessage(text='最多三人哦')
        else:
            message = create_answer_nb()
            line_bot_api.reply_message(event.reply_token, message)
    elif data == 'disband':
        if col_game.find_one() != None:
            message = []
            FlexMessage = json.load(open('yesno.json'))
            message.append(TextSendMessage(text='重新遊戲 ?'))
            message.append(FlexSendMessage('ok', FlexMessage))
            line_bot_api.reply_message(event.reply_token, message)
        else:
            message = TextSendMessage(text='早就清零了別再按了!')
            line_bot_api.reply_message(event.reply_token, message)
    elif data == 'disband_nb':
        if col_gr.find_one() != None:
            message = []
            FlexMessage = json.load(open('yesno_nb.json'))
            message.append(TextSendMessage(text='重新開始 ?'))
            message.append(FlexSendMessage('ok', FlexMessage))
            line_bot_api.reply_message(event.reply_token, message)
        else:
            message = TextSendMessage(text='早就沒人別再按了!')
            line_bot_api.reply_message(event.reply_token, message)
    elif data == 'exit':
        nid = get_profile(event)['name']
        uid = get_profile(event)['user_id']
        col_game.delete_one({'name': nid, 'user_id': uid})
        message = TextSendMessage(text=f'{nid} 離開遊戲囉!')
        line_bot_api.reply_message(event.reply_token, message)
    elif data == 'yes':
        if col_game.find_one() != None:
            message = clear_guessgame()
            line_bot_api.reply_message(event.reply_token, message)
        else:
            message = TextSendMessage(text='早就沒人別再按了!')
            line_bot_api.reply_message(event.reply_token, message)
    elif data == 'yes_nb':
        if col_gr.find_one() != None:
            message = clear_gg()
            line_bot_api.reply_message(event.reply_token, message)
        else:
            message = TextSendMessage(text='早就沒人別再按了!')
            line_bot_api.reply_message(event.reply_token, message)
    elif data == 'no':
        if col_game.find_one() == None:
            message = TextSendMessage(text='目前無人加入')
        else:
            message = TextSendMessage(text='遊戲繼續')
        line_bot_api.reply_message(event.reply_token, message)
    elif data == 'no_nb':
        if col_gr.find_one() == None:
            message = TextSendMessage(text='目前無人')
        else:
            message = TextSendMessage(text='遊戲繼續')
        line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
