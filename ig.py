import json
import requests
from lxml import etree

# Reference
# https://dev.to/iankerins/the-easy-way-to-build-an-instagram-spider-using-python-scrapy-graphql-4gko

## meme library
everday_a_meme = "https://www.instagram.com/everyday.a.meme/"
dank_meme_therapy = "https://www.instagram.com/dank_meme_therapy/"
gokusanmemes = "https://www.instagram.com/gokusanmemes/"
memes = "https://www.instagram.com/memes/"
hell_yeah_meme67 = "https://www.instagram.com/hell_yeah_meme67/"
dank_memes_0610 = "https://www.instagram.com/dank_memes_0610/"
memezar = "https://www.instagram.com/memezar/"
animemes_taiwan = "https://www.instagram.com/animemes.taiwan/"
memes_engineering_69 = "https://www.instagram.com/memes_engineering_69/"
meme_boof = "https://www.instagram.com/meme.boof/"
hoodentertainmentclub = "https://www.instagram.com/_hoodentertainmentclub_/"
grad_school_memes = "https://www.instagram.com/grad.school.memes/"
clerkmeme9487 = "https://www.instagram.com/clerkmeme9487/"
meme2020 = "https://www.instagram.com/meme2020/"
memecoding = "https://www.instagram.com/meme_coding/"
memeviz = "https://www.instagram.com/memeviz/"
meme_necessities = "https://www.instagram.com/meme_necessities/"
busimeme = "https://www.instagram.com/busimeme/"

# meme hashtags
meme1 = "https://www.instagram.com/explore/tags/memes😂/"
meme2 = "https://www.instagram.com/explore/tags/memes/"
meme3 = "https://www.instagram.com/explore/tags/meme/"
meme4 = "https://www.instagram.com/explore/tags/dankmemes/"
meme5 = "https://www.instagram.com/explore/tags/memesdaily/"
meme6 = "https://www.instagram.com/explore/tags/memestagram/"
meme7 = "https://www.instagram.com/explore/tags/memer/"
meme8 = "https://www.instagram.com/explore/tags/memegod/"

# add to list
meme_page_library = [everday_a_meme,dank_meme_therapy,gokusanmemes,memes,hell_yeah_meme67,dank_memes_0610,memezar,animemes_taiwan,memes_engineering_69,meme_boof,hoodentertainmentclub,grad_school_memes,clerkmeme9487,meme2020,memecoding,memeviz,meme_necessities,busimeme]
meme_hashtag_library = [meme1,meme2,meme3,meme4,meme5,meme6,meme7,meme8]


def get_url(url):   
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Access approved...")
            return response.text
        else:    
            print(response.status_code)        
    except Exception as e:
        print(e)
        return None


def get_posts(url,status):
    print("Executing....")
    html = get_url(url)
    if type(html) == str:
        selector = etree.HTML(html)
        links = selector.xpath("//script[starts-with(.,'window._sharedData')]/text()")[0]
        json_string = links.strip().split("= ")[1][:-1]
        data = json.loads(json_string)

        if status == "profile":
            edges = data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
        elif status == "hashtag":
            edges = data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_top_posts']['edges']
        url = []
        for edge in edges:
            display_url = edge['node']['display_url']
            print(display_url)
            url.append(display_url)
    return url


# cronjob for everyday
# add try except later

current_urls = []
for mp in meme_page_library:
    current_urls += get_posts(mp,"profile")
for mhl in meme_hashtag_library:
    current_urls += get_posts(mhl,"hashtag")

current_urls = pd.DataFrame({"meme_url": current_urls})

# merging
existing_urls = pd.read_csv("urls.csv")
current_urls = pd.concat([current_urls.existing_urls])
current_urls = pd.DataFrame({'meme_url': current_urls['meme_url'].unique()})

# outputting and saving
current_urls.to_csv("urls.csv",index=False , sep=",")





