# Line控制台
#https://account.line.biz/login?redirectUri=https%3A%2F%2Fdevelopers.line.biz%2Fconsole%2F&scope=line


## https://markteaching.com/create-line-bot/
## https://github.com/line/line-bot-sdk-python 
## https://ithelp.ithome.com.tw/articles/10196397

# Chatbot manager 功能
# https://ithelp.ithome.com.tw/articles/10195333

## Building image map
# https://ithelp.ithome.com.tw/articles/10195640
 
## 範例串接起來的bot
## https://medium.com/@skywalker0803r/line-bot助手機器人實作-893e24db0ab5


## Database
#https://ithelp.ithome.com.tw/articles/10221847


# Line official manager account
#https://manager.line.biz/account/@902mlsrz/autoresponse/welcome
#https://manager.line.biz/account/@902mlsrz/richmenu/2608685

## Send不同message
## https://blackmaple.me/line-bot-tutorial/

# imports


from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

# import modules

from bs4 import BeautifulSoup
from lxml import etree

import random
import re
import requests
import json
import pandas as pd
## import self defined scipts
import laugh
from jokes import Yams
from jokes import PttJokes



app = Flask(__name__)

# Channel Access Token
## don't know why but config doesn't work
line_bot_api = LineBotApi("/4oIMZ54i6LWr+X3z/c1o6X6p0K7FbD0bv+A0Ob992QxdfjYFvFrFaoYVw/yytxHxkKQnzUYxRS+58j39u+TrnMB4jSsxBVgzp0evMemMGnOp4UzH11HPtR06QEhBC+NhNRd4NQnHzjeiHTv71ZZIQdB04t89/1O/w1cDnyilFU=")
# Channel Secret
handler = WebhookHandler("295c255eebeac52faedb901f2e85096a")


'''
# LINE 聊天機器人的基本資料
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
print(line_bot_api)
print(handler)
'''

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body, "Signature: " + signature)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

    ## get userid
    #profile = line_bot_api.get_profile(event['events'][0]['source']['userId'])
    #print(profile)

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
## 當收到 LINE 的 MessageEvent (信息事件)，而且信息是屬於 TextMessage (文字信息)的時候，就執行下列程式碼
def handle_message(event):
    #該函數會接收一個 LINE 發送過來的資訊，並貼上event的標籤，方便後續的操作
    msg = event.message.text
    msg = msg.strip()
    choose =['日常生活','純粹梗圖','日常垃圾話','政治吐嘈','工作','ACG相關、補番、吐槽','遊戲梗','校園生活','時事']

    
    if msg =="貼圖":
        reply = StickerSendMessage(package_id=str(random.randint(1,4)),sticker_id=str(random.randint(1,17)))
        line_bot_api.reply_message(event.reply_token, reply)

    elif msg.strip() == "我要網路梗圖！":
        message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://www.flaticon.com/svg/static/icons/svg/3077/3077000.svg',
                        title='Meme Category 1',
                        text='日常生活類',
                        actions=[
                            MessageTemplateAction(
                                label=choose[0],
                                text=choose[0]
                            ),
                            MessageTemplateAction(
                                label=choose[7],
                                text=choose[7]
                            ),
                            MessageTemplateAction(
                                label=choose[1],
                                text=choose[1]
                            )
 
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://www.flaticon.com/svg/static/icons/svg/68/68299.svg',
                        title='Meme Category 2',
                        text='政治、時事、工作',
                        actions=[
                            MessageTemplateAction(
                                label=choose[3],
                                text=choose[3]
                            ),
                            MessageTemplateAction(
                                label=choose[8],
                                text=choose[8]
                            ),
                            MessageTemplateAction(
                                label=choose[4],
                                text=choose[4]
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://www.flaticon.com/svg/static/icons/svg/3616/3616441.svg',
                        title='Meme Category 3',
                        text='垃圾話、遊戲',
                        actions=[
                            MessageTemplateAction(
                                label=choose[2],
                                text=choose[2]
                            ),
                            MessageTemplateAction(
                                label=choose[6],
                                text=choose[6]
                            ),
                            MessageTemplateAction(
                                label=choose[5],
                                text=choose[5]
                            )
                        ]
                    )
                ],
                image_size="contain"
            )
        )
        line_bot_api.reply_message(event.reply_token, message)

    elif msg in choose:

        print("Buttons Template")
        category_dict = {'日常生活':29,'純粹梗圖':53,'日常垃圾話':6,'政治吐嘈':8,'工作':86,'ACG相關、補番、吐槽':17,'遊戲梗':94,'校園生活':11,'時事':35}
        #re.search("梗圖",msg)==True:
        #category = random.sample([29,53,6,8,86,17,94,11,35],1)[0]

        category = category_dict[msg]
        result = laugh.GetMemes(category,1) 
        r = result[0]
        print(r,type(r))
        reply = ImageSendMessage(
            original_content_url=r,
            preview_image_url=r)
        line_bot_api.reply_message(event.reply_token, reply)

        # push message can push up to 5 messages
        #line_bot_api.push_message(to, TextSendMessage(text='Hello World!'))
    elif msg == "我要笑話！":

        joke_dict = {"NewJoke":"http://kids.yam.com/joke/newjoke.php?page=","TopJoke":"http://kids.yam.com/joke/topjoke.php?page=","AnimalJoke":"http://kids.yam.com/joke/cat.php?cid=animal&page=","CampusJoke":"http://kids.yam.com/joke/cat.php?cid=campus&page=","GeneralJoke":"http://kids.yam.com/joke/cat.php?cid=general&page"}

        joke_page_num = {"NewJoke":[1,7],"TopJoke":[1,7],"AnimalJoke":[1,131],"CampusJoke":[1,400],"GeneralJoke":[1,1642]}

        ## if random outputs 0 --> Yams
        select = random.randint(0,1)

        if select == 0:

            category = random.sample(joke_dict.keys(),1)[0]
            Yams_cateogry = Yams(category,1)
            output = Yams_cateogry.output()
            reply = TextSendMessage(text = output)
            line_bot_api.reply_message(event.reply_token,reply)
       ## if random output 1 ---> Ptt Jokes
        elif select ==1:

            Pttjokes = PttJokes(1)
            output = Pttjokes.output()
            reply = TextSendMessage(text = output)
            line_bot_api.reply_message(event.reply_token,reply)
        
    elif msg == "我要IG梗圖！":
        #random choose
        urls = pd.read_csv("urls.csv")
        index = random.randint(1,urls.shape[0])
        return_url = urls.iloc[index,0]
        reply = ImageSendMessage(
            original_content_url=return_url,
            preview_image_url=return_url)
        line_bot_api.reply_message(event.reply_token, reply)

    else:
        reply = TextSendMessage(text = msg)
        ## event.reply token 用完一次即消失
        line_bot_api.reply_message(event.reply_token,reply)


@app.route('/')
def index():
    return 'Hello World'

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)















