## 笑話linebot
## 梗圖linebot



##Meme 梗圖倉庫
# MemeBank
# https://memes.tw/wtf?contest=29&page=1

import requests
from bs4 import BeautifulSoup
import time
import random

'''
#0 日常生活    contest = 29  1-230
#1 純粹梗圖    contest = 53  1-122
#2 日常垃圾話  contest = 6   1-86
#3 政治吐嘈    contest=8		1-166
#4 工作       contest=86	1-27
5 ACG相關、補番、吐槽 contest=17  1-16
6 遊戲梗     contest=94   1-61
#7 校園生活   contest=11	    1-96
#8 時事		contest=35	1-33
'''


#url = "https://memes.tw/wtf?contest=29&page="

def get_urls(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:    
            print('请求错误状态码：', response.status_code)
            return "Error"    
    except Exception as e:
        print(e)
        return None


## 日常生活

def GetMemes(category,number):

	if category==29:
		page_restriction = [1,230]
	elif category==53:
		page_restriction = [1,122]
	elif category==6:
		page_restriction = [1,86]	
	elif category==8:
		page_restriction = [1,166]	
	elif category==86:
		page_restriction = [1,27]	
	elif category==17:
		page_restriction = [1,16]	
	elif category==94:
		page_restriction = [1,61]	
	elif category==11:
		page_restriction = [1,96]	
	elif category==35:
		page_restriction = [1,33]		
	i = random.randint(page_restriction[0],page_restriction[1])
	url = "https://memes.tw/wtf?"+"contest="+str(category)+"page="+str(i)
	## Save all links
	images_links = []

	while get_urls(url)!="Error":
		
		response_text = get_urls(url)
		html = BeautifulSoup(response_text, 'html.parser')
		images = html.find_all('img')
		
		images_TF = list(map(lambda x:x.has_attr('data-src'), images))
		
		for tf in range(len(images_TF)):
			if images_TF[tf] ==True:
				images_links.append(images[tf]['data-src'])
		
		#print(images_links)
		#print(len(images_links))
		print("Page",i)
		
		if len(images_links)>number:
			output = random.sample(images_links,number)
			print("+++++++++ Done +++++++++")
			break
		else:
			i = random.randint(page_restriction[0],page_restriction[1])
			url = "https://memes.tw/wtf?"+"contest="+str(category)+"page="+str(i)
	return output


# ok







