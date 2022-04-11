from random import shuffle,randint
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *


def random_bot2v():
    from random import shuffle
    list = ['1', '2', '3', '4']
    shuffle(list) #重排序
    n = 2 #分成n組
    m = int(len(list)/n)
    list4 = []
    for i in range(0, len(list), m):
        list4.append(list[i:i+m])
    a = sorted(list4[0])
    b = sorted(list4[1]) 
    list_v = "".join(a) + " | " + "".join(b)
    return list_v

def random_bot3v():
    from random import shuffle
    list = ['1', '2', '3', '4', '5', '6']
    shuffle(list) #重排序
    n = 2 #分成n組
    m = int(len(list)/n)
    list4 = []
    for i in range(0, len(list), m):
        list4.append(list[i:i+m])
    a = sorted(list4[0])
    b = sorted(list4[1]) 
    list_v = "".join(a) + " | " + "".join(b)
    return list_v


def random_bot4v():
    from random import shuffle
    list = ['1', '2', '3', '4', '5', '6', '7', '8']
    shuffle(list) #重排序
    n = 2 #分成n組
    m = int(len(list)/n)
    list4 = []
    for i in range(0, len(list), m):
        list4.append(list[i:i+m])
    a = sorted(list4[0])
    b = sorted(list4[1]) 
    list_v = "".join(a) + " | " + "".join(b)
    return list_v


def response_wadu():
    response_list=['早阿','你好','不早了','我寒兒','哈囉好久不見','都幾點了還早','傻孩子早','不要理我'
    ,'又再早','早爽沒','我要睡了掰','一直被你們吵醒，我要去睡了','歐嗨唷']
    shuffle(response_list)
    list_word=response_list[0]
    str_word=''.join(list_word)
    return str_word







