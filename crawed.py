from typing import Text
from bs4 import BeautifulSoup
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

import requests 

def ptt_templat():
    message = TemplateSendMessage(
        alt_text='最新PTT內容',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/4LPtTTc.jpg?1',
            title='PTT最新文章',
            text='安心食用',
            actions=[
                PostbackTemplateAction(
                    label='八卦版',
                    data='5'
                ),
                PostbackTemplateAction(
                    label='表特版',
                    data='6'
                ),
                PostbackTemplateAction(
                    label='電影版',
                    data='7'
                ),
                PostbackTemplateAction(
                    label='股市版',
                    data='8'
                )
            ]
        )
    )
    return message



def gossiping_ptt():
    request_html = requests.get("https://www.ptt.cc/bbs/Gossiping/index.html",headers={"cookie":"over18=1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"})
    request_html.encoding = 'uft-8'
    soup = BeautifulSoup(request_html.text, "html.parser") 
    titles = soup.find_all("div",class_="title")

    ## 印出排好版的HTML架構
    content = ""
    for title in titles:
        if title.a != None:
            link = title.select_one("a").get("href")
            title_ptt = title.select_one("a").getText()
            content += '{}\n{}\n'.format(title_ptt, "https://www.ptt.cc"+link)
    return content



def beauty_ptt():
    request_html = requests.get("https://www.ptt.cc/bbs/Beauty/index.html",headers={"cookie":"over18=1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"})
    request_html.encoding = 'uft-8'
    soup = BeautifulSoup(request_html.text, "html.parser") 
    titles = soup.find_all("div",class_="title")

    ## 印出排好版的HTML架構
    content = ""
    for title in titles:
        if title.a != None:
            link = title.select_one("a").get("href")
            title_ptt = title.select_one("a").getText()
            content += '{}\n{}\n'.format(title_ptt, "https://www.ptt.cc"+link)
    return content



def moive_ptt():
    request_html = requests.get("https://www.ptt.cc/bbs/movie/index.html",headers={"cookie":"over18=1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"})
    request_html.encoding = 'uft-8'
    soup = BeautifulSoup(request_html.text, "html.parser") 
    titles = soup.find_all("div",class_="title")

    ## 印出排好版的HTML架構
    content = ""
    for title in titles:
        if title.a != None:
            link = title.select_one("a").get("href")
            title_ptt = title.select_one("a").getText()
            content += '{}\n{}\n'.format(title_ptt, "https://www.ptt.cc"+link)
    return content



def stock_ptt():
    request_html = requests.get("https://www.ptt.cc/bbs/Stock/index.html",headers={"cookie":"over18=1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"})
    request_html.encoding = 'uft-8'
    soup = BeautifulSoup(request_html.text, "html.parser") 
    titles = soup.find_all("div",class_="title")

    ## 印出排好版的HTML架構
    content = ""
    for title in titles:
        if title.a != None:
            link = title.select_one("a").get("href")
            title_ptt = title.select_one("a").getText()
            content += '{}\n{}\n'.format(title_ptt, "https://www.ptt.cc"+link)
    return content



def moive():
    request_html = requests.get("https://movies.yahoo.com.tw/movie_comingsoon.html",headers={"cookie":"over18=1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"})
    request_html.encoding = 'uft-8'
    soup = BeautifulSoup(request_html.text, "html.parser") 
    info_items = soup.find_all('div', 'release_info')
    content = ""
    for item in info_items:
        movie_name = item.find('div', 'release_movie_name').a.text.strip()
        english_name = item.find('div', 'en').a.text.strip()
        release_time = item.find('div', 'release_movie_time').text.split('：')[-1].strip()
        content += f'{movie_name}\n{english_name}\n上映日:{release_time}\n------------------\n'
    return content



def GetWeather(station):
    end_point= "https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0001-001?Authorization=CWB-A717DED8-4CD4-4005-8F93-72B183B0D61A&format=JSON"
    data = requests.get(end_point).json()
    data = data["records"]["location"]
    target_station = "not found"
    for item in data:
        if item["locationName"] == str(station):
            target_station = item
    return target_station



def MakeRailFall(station):
    result = requests.get(
        "https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0002-001?Authorization=CWB-A717DED8-4CD4-4005-8F93-72B183B0D61A&format=JSON")
    msg = ""
    if(result.status_code != 200):
        return "雨量資料讀取失敗"
    else:
        railFallData = result.json()
        for item in railFallData["records"]["location"]:
            if station in item["locationName"]:
                msg += "雨量：" + \
                    item["weatherElement"][7]["elementValue"] + "mm"
                return msg
        return "查無此測站"



def MakeWeather(station):
    WeatherData = GetWeather(station)
    if WeatherData == "not found":
        return False
    Weather_Data = WeatherData["weatherElement"]
    Weather_Time = WeatherData["time"]["obsTime"]
    msg = "測站：" + station
    msg += "\n時間：" + Weather_Time 
    msg += "\n溫度：" + Weather_Data[3]["elementValue"] + "℃\n"
    msg += "濕度：" + \
        str(float(Weather_Data[4]["elementValue"]) * 100) + "% \n"
    msg += "風向：" + Weather_Data[1]["elementValue"] + "°\n"
    msg += "風速：" + Weather_Data[2]["elementValue"] + "m/s\n"
    msg += MakeRailFall(station) + "\n\n"
    msg += "資料來源：中央氣象局\n註：此為目標地區方圓5公里最近的測站"
    return msg



def MakeAQI(location):
    end_point = "https://data.epa.gov.tw/api/v1/aqx_p_432?api_key=9be7b239-557b-4c10-9775-78cadfc555e9" 
    data = requests.get(end_point)
    AQImsg = ""
    if data.status_code == 500:
        return "無 AQI 資料"
    else:
        for i in range(84):
            AQIdata = data.json()["records"][i]
            if AQIdata["SiteName"] == str(location):
                AQImsg += "測站："+ location + "\n"
                AQImsg += "時間："+ AQIdata["PublishTime"] + "\n"
                AQImsg += "空氣指標：" + AQIdata["AQI"] + "\n"
                AQImsg += "空氣品質：" + AQIdata["Status"] + "\n"
                AQImsg += "PM2.5：" + AQIdata["PM2.5"] + "ug/m3"
                AQImsg += "\n\n資料來源：環保署"
        return AQImsg



def Earthquake():
    end_point = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0016-001?Authorization=CWB-E7F025FB-4BBF-476E-9251-454E9D3FC2E0&limit=10&format=JSON"
    data = requests.get(end_point)
    earthquake_msg = ""
    if data.status_code == 500:
        return "無地震資料"
    else:
        earthquake_data = data.json()["records"]["earthquake"][0]
        earthquake_msg += f'地震報告：{earthquake_data["reportContent"]}\n'
        return earthquake_msg
            


def Covid():
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
    msg += "全台累計確診：" + today_stat + "人\n"
    other_first = titles[0].text
    msg += "本土病例："+ other_first + "人\n"
    other_second = titles[1].text
    msg += "境外移入：" + other_second + "人\n"
    other_third = titles[2].text
    msg += "死亡病例：" + other_third + "人\n\n"
    msg += "資料來源：衛福部網站"
    return msg
