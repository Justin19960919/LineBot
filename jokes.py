import requests
from bs4 import BeautifulSoup
import time
import random

## 全域的function
def Access_and_GetHtml(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            
            required_html = BeautifulSoup(response.text, 'html.parser')
            return required_html
        else:    
            print('请求错误状态码：', response.status_code)
            return "Error"    
    except Exception as e:
        print(e)
        return None



######################### Yams Jokes ###########################
joke_dict = {"NewJoke":"http://kids.yam.com/joke/newjoke.php?page=","TopJoke":"http://kids.yam.com/joke/topjoke.php?page=","AnimalJoke":"http://kids.yam.com/joke/cat.php?cid=animal&page=","CampusJoke":"http://kids.yam.com/joke/cat.php?cid=campus&page=","GeneralJoke":"http://kids.yam.com/joke/cat.php?cid=general&page"}

joke_page_num = {"NewJoke":[1,7],"TopJoke":[1,7],"AnimalJoke":[1,131],"CampusJoke":[1,400],"GeneralJoke":[1,1642]}




class Yams:
    
    # 小蕃薯笑話
    # 新鮮笑話
    # http://kids.yam.com/joke/newjoke.php?page=1
    # 爆笑排行
    # http://kids.yam.com/joke/topjoke.php
    # 動物笑話
    # http://kids.yam.com/joke/cat.php?cid=animal
    # 校園笑話
    # http://kids.yam.com/joke/cat.php?cid=campus
    # 一般笑話
    # http://kids.yam.com/joke/cat.php?cid=general

    def __init__(self,category,number):

        self.category = category
        self.number = number

    def GetJoke(self,link):

        joke_html = Access_and_GetHtml(link)    
        joke_title = joke_html.find("td","boardtitle2").text
        joke_info = joke_html.find("td","tableword2").text
        ## maybe strip all \n
        all_joke = "--------"+joke_title +"--------"+ joke_info+'\n'+'\n'
        return(all_joke)

    def GetPageUrl(self,page):
        
        page_html = Access_and_GetHtml(page) 
        page_jokes = page_html.find_all('a','purple')
        jokes_url = list(map(lambda x:"http://kids.yam.com/joke"+x['href'].lstrip("."), page_jokes))
        #print(jokes_url)
        #joke_info = list(map(lambda x:GetJoke(x), jokes_url))

        return(jokes_url)

    def output(self):

        output = ""
        page_links=[]

        while len(page_links) < self.number:
            
            link = joke_dict[self.category]+str(random.randint(joke_page_num[self.category][0],joke_page_num[self.category][1]))

            page_links += self.GetPageUrl(link)

        final_page_links = random.sample(page_links,self.number)

        for pl in final_page_links:
            output += self.GetJoke(pl)

        return output

#yams_test=Yams("NewJoke",1)
#print(yams_test.output())
# test succeed


############################## Ptt Jokes ###########################


class PttJokes:

    def __init__(self,number):
        self.number = number

    def GetPttJoke(self,link):
        ## get html 

        pttjoke_html = Access_and_GetHtml(link) 

        if pttjoke_html!= "Error" or ptt_page != None:
            firstblock = pttjoke_html.select('.article-meta-value')
            author = firstblock[0].text
            topic= firstblock[2].text
            date = firstblock[3].text

            split_text = u'※ 發信站: 批踢踢實業坊(ptt.cc),'

            ## get main content
            initial_content = pttjoke_html.find(id="main-content").text
            content = initial_content.split(split_text)
            content = content[0].split(date)
            content = content[1].split('--')
            content = content[0].rstrip(" ")
            main_content = content.lstrip(" ")
            output_format = "標題: "+topic+""+'\n'+main_content+author+date+" From ptt"+"\n"

            return output_format
        else:
            return " "

    def PTT_page(self,page):



        ptt_header = "https://www.ptt.cc/bbs/joke/index"+str(page)+".html"
        ptt_page=Access_and_GetHtml(ptt_header)



        if ptt_page != "Error" or ptt_page !=None:
            
            title_and_link = ptt_page.select("div.title > a")
            
            post_url = list(map(lambda x:"https://www.ptt.cc"+x.get('href'), title_and_link))
            post_name = list(map(lambda x:x.text.rstrip(" "), title_and_link))

            ## not replies of other posts, returns True
            not_reply = list(map(lambda x:x[:2]!="Re", post_name))
            #print(not_reply)


            output_dict={post_name[index]:post_url[index] for index in range(len(not_reply)) if not_reply[index]==True}

            return output_dict
            
        else:
            return None
    
    def output(self):

        current_number_of_jokes = 0
        output = ""
        need_jokes = self.number

        while current_number_of_jokes < self.number:

            # Currently hard code to page 7249, need to change to adaption.
            random_page = random.randint(2,7249)
            page_output = self.PTT_page(random_page)
            
            ## number of jokes available
            jokes_in_this_page =len(page_output.keys())
            current_number_of_jokes += jokes_in_this_page

            if jokes_in_this_page > need_jokes:

                ##  sample enough needed jokes
                random_keys= random.sample(page_output.keys(),need_jokes)

                for rk in random_keys:
                    output += self.GetPttJoke(page_output[rk])

                break
            ## if jokes in this page is less than requested
            else:

                for normal in page_output.keys():
                    output += self.GetPttJoke(page_output[normal])

                need_jokes -= current_number_of_jokes
        ## should output text of required number of jokes
        return output



#ptt = PttJokes(1)
#print(ptt.output())
# test succeed




print(random.randint(0,1))






