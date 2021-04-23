import json
import requests
import pandas as pd
import datetime
import os
import time

# Using Rapid API to fetch instagram posts
class getPosts:

    RAPID_API_ENDPOINT = "https://instagram47.p.rapidapi.com/user_posts"
    RAPID_API_KEY = "0c7074abe6msh8f13c4bd42a83abp1c441djsnd0657cbc3cfe"
    RAPID_API_HOST = "instagram47.p.rapidapi.com" 

    def __init__(self, username):
        self.items = self.preprocess(self.fetch(username))   # list of items that are fetched


    def fetch(self, user_name):
        try:
            user_name = user_name.strip()   # just strip front and end whitespaces in case
            print(f"Using rapid API to send requests regarding Instagram account: {user_name}...")
            querystring = {"username": user_name}
            headers = {
                'x-rapidapi-key': self.RAPID_API_KEY,
                'x-rapidapi-host': self.RAPID_API_HOST 
                }
            response = requests.request("GET", self.RAPID_API_ENDPOINT, headers=headers, params=querystring)
            return json.loads(response.text)
        except:
            print("Unfortunately there occurred an error..")
            return {}    
        
    def preprocess(self, response_dict):
        if 'status' in response_dict and response_dict['status'] == "Success":
            print("Status of response is success, we are good to go..")
            return response_dict['body']['items']
        
        print('Status of response is not success')
        return None
    
    def getVideoUrlFromItem(self, item):
        if 'video_versions' in item:
            # we have a video post
            vids = item['video_versions']    
            if len(vids) >= 1:
                vid_url = vids[0]['url']
                return vid_url
        return ''

    def getImageUrlFromItem(self, item):
        if 'image_versions2' in item:
            images = item['image_versions2']
            if len(images) >= 1:
                image_url = images['candidates'][0]['url']
                return image_url
        return ''

    def getAllUrls(self):
        if self.items is not None:
            video_urls = list(map(lambda x: self.getVideoUrlFromItem(x), self.items))
            image_urls = list(map(lambda x: self.getImageUrlFromItem(x), self.items))
            # reduce
            return self.cleanUrls(video_urls) + self.cleanUrls(image_urls)
        
        # if is None shouldn't be here
        print("Fetching failed, plz try another url... ")
        return None

    def cleanUrls(self,urls):
        urls_result = []
        for url in urls:
            if url != '':
                urls_result.append(url)
        return urls_result


def crawlAllAccounts(listOfAccounts):
    allUrls = []
    for account in listOfAccounts:
        posts = getPosts(account)
        posts_urls = posts.getAllUrls()
        if posts_urls != None:
            allUrls += posts_urls
        print("Sleeping for 10 seconds")
        time.sleep(10)   # slow down
    print("Finished crawling all accounts...")
    return allUrls



# url_list: list of urls, save to csv file
def saveToCsv(url_list):
    # get datetime
    now = datetime.datetime.now()
    timestamp = f"{now.year}-{now.month}-{now.day}" 
    df = pd.DataFrame({'date': timestamp, 'meme_url': url_list})
    # concat
    if os.path.exists('urls.csv'):
        original_df = pd.read_csv('urls.csv')
        frames = [original_df, current_df]
        print("Concatenating old df with new df...")
        df = pd.concat(frames)
        print("Dropping duplicates...")
        df = df.drop_duplicates(subset = ["meme_url"])
        print('Writing to csv file...')
        df.to_csv("urls.csv", index=False, sep=",")
    else:
        df.to_csv("urls.csv", index=False, sep=",")
    


# whole flow
# specify all username of account here
meme_list = ['everyday.a.meme', 'dank_meme_therapy', 'gokusanmemes', 'grad.school.memes','memes_engineering_69', 'sarcastic_lines', 'meme_coding', 'memeviz','epicfunnypage','fuckjerry', 'sarcasm_only', 'daquan', 'thefatjewish', 'lmao', 'societyfeelings', 'couplesnote', 'funnymemes', 'ladbible','hell_yeah_meme67', 'animemes_taiwan']  
# for test only
# meme_list = ['epicfunnypage','fuckjerry', 'sarcasm_only']
allUrls = crawlAllAccounts(meme_list)
saveToCsv(allUrls)




