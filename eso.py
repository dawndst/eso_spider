import requests, json, os
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

cur_dir = os.path.dirname(__file__)


HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'Connection':'keep-alive',
    'Content-Type':'text/html; charset=utf-8',
    #'Host':'live.kuaishou.com',
    #'Cookie':'did=web_1289764fb4314b649a333c162ba0c069; didv=1671852980000; clientid=3; kuaishou.live.bfb1s=3e261140b0cf7444a0ba411c6f227d88; client_key=65890b29; kpn=GAME_ZONE; kpn=GAME_ZONE; ksliveShowClipTip=true',
    #'Cookie':'did=web_1289764fb4314b649a333c162ba0c069; didv=1671852980000; clientid=3; kuaishou.live.bfb1s=3e261140b0cf7444a0ba411c6f227d88; client_key=65890b29; kpn=GAME_ZONE; kpn=GAME_ZONE; ksliveShowClipTip=true; _did=web_24709210813A95F4; userId=2344108852; kuaishou.live.web_st=ChRrdWFpc2hvdS5saXZlLndlYi5zdBKgAfc4AdFw8PV3vqmdjk7U5hg3g9qf5xpAkDeVNQmYGCRTaXMm3VsNJWwG9JHsXsXIkmGEtHb-IG709Ve-gE1OXLcAM548njhnZfdkg9MdqxFe7t1OaCd25V6xJT7xjSnYBw2GYh9IQzdgqfJa5od2dLHKHY_FDlcQ8TgKL470Yb09fM5ub8kVobu0DBiRfVoNSrZX7CCzvFvSOh2GquZmPqQaEpGRdADNj0HroX-OzPO0ZFU2uiIgDF6aZxPggJ4-J4ie3XaxxOk6rl0f86zHgE2mCJAvOY8oBTAB; kuaishou.live.web_ph=524893456f5fbf8b832c20ba7e3419d5dcfe; userId=2344108852',
    }   


URL_DICT = {}
URL_DICT = {'/en-us/crownstore': 'Featured ', '/en-us/crownstore/eso-plus': 'ESO Plus Deals ', '/en-us/crownstore/category/36': 'Special Offers ', '/en-us/crownstore/category/38': 'Crown Crates ', '/en-us/crownstore/category/1': 'DLC ', '/en-us/crownstore/category/71': 'Quest Starters ', '/en-us/crownstore/category/7': 'Upgrades ', '/en-us/crownstore/category/3': 'Utility ', '/en-us/crownstore/category/56': 'Houses ', '/en-us/crownstore/category/62': 'Furniture ', '/en-us/crownstore/category/52': 'Style Parlor ', '/en-us/crownstore/category/17': 'Crafting ', '/en-us/crownstore/category/6': 'Wardrobe ', '/en-us/crownstore/category/4': 'Mounts ', '/en-us/crownstore/category/5': 'Non-Combat Pets '}
BASE_URL = 'https://www.elderscrollsonline.com/'

def init_category(url, name):
    print('Processing %s' % (BASE_URL+url))

    df = pd.DataFrame(columns=['L1_Title', 'L2_Title', 'Item_Name', 'Image_URL'])


    result = requests.get(BASE_URL+url, headers = HEADERS)
    bs = BeautifulSoup(result.text, "html.parser")
    
    container = bs.find_all('div', class_='col-xs-12')

    for item in container:
        if len(item.attrs['class']) == 1:
            break
    
    subtitle_list = item.find_all(class_= 'section-header text-center')
    item_list = item.find_all(class_ = 'row')

    if len(subtitle_list) != len(item_list):
        return

    for index in range(0, len(subtitle_list), 1):
        title = subtitle_list[index].find(class_ = 'title').contents[0]
        print(title)
        
        news_snip_list = item_list[index].find_all(class_ = 'news-snip')

        for news_snip in news_snip_list:
            t = news_snip.find(class_ = 'img-responsive')
            img_url = t.attrs['data-lazy-src']
            #

            hasDayLeft = False
            hasPercentLeft = False
            hasNew = False

            #has limit time offer
            corner_flag = news_snip.find(class_ = 'crown-flag lto text-center countdown')
            if corner_flag:
                hasDayLeft = True
                data_timestamp = corner_flag.attrs['data-timestamp']
                day_left = news_snip.find(class_ = 'time-left')

            corner_flag = news_snip.find(class_ = 'crown-flag new text-center')
            if corner_flag:
                hasNew = True
            
            corner_flag = news_snip.find(class_ = 'crown-flag text-center countdown')
            if not corner_flag:
                corner_flag = news_snip.find(class_ = 'crown-flag text-center')

            if corner_flag:
                hasPercentLeft = True
                data_timestamp = corner_flag.attrs['data-timestamp']
                day_left = news_snip.find(class_ = 'time-left')
    
                discount = corner_flag.contents[2]
        

            t = news_snip.find(class_ = 'crown-title')
            crown_title = t.contents[0]
            print(crown_title)

            t = news_snip.find(class_ = 'epd-label')
            if t:
                deal = t.contents[0]


            #price
            gems_price_area = news_snip.find(class_ = 'gems-price')
            if gems_price_area:
                gem_normal = gems_price_area.find(class_ = 'bright crown-details').contents[0]
                if hasDayLeft:
                    gem_deal = gems_price_area.find_all(class_ = 'sr-only')
            #print(gem_normal)
            #print(gem_deal[1].contents[0])


            seals_price_area = news_snip.find(class_ = 'seals-price')
            if seals_price_area:
                seals_normal = seals_price_area.find(class_ = 'bright crown-details').contents[0]
                if hasDayLeft:
                    seals_deal = seals_price_area.find_all(class_ = 'sr-only')


            crown_price_area = news_snip.find(class_ = 'crowns-price')
            if crown_price_area:
                if not hasPercentLeft:
                    if hasNew:
                        print('has new--------------')
                    else:
                        crown_normal = crown_price_area.find(class_ = 'bright crown-details').contents[0]
                        print(crown_normal)
                else:
                    #has strike price
                    crown_normal = crown_price_area.find(class_ = 'strike').contents[0]
                    crown_deal = crown_price_area.find(class_ = 'crown-details').contents[1]
        
            df = pd.concat([pd.DataFrame([[name, title, crown_title, img_url]], columns=df.columns), df], ignore_index=True)

    dt = datetime.today().date()
    filename = 'eso_%s_%s.xlsx' % (name, dt)
    df.to_excel(os.path.join(cur_dir, filename))

def init():
    result = requests.get('https://www.elderscrollsonline.com/en-us/crownstore/category/7', headers = HEADERS)
    bs = BeautifulSoup(result.text, "html.parser")   

    heading_list = bs.find_all(class_ = 'accordion-heading')
    body_list = bs.find_all('ul', class_ = 'accordion-body')

    global URL_DICT
    for i in range(0, len(heading_list), 1):
        heading_item = heading_list[i]
        body_item = body_list[i]


        t = heading_item.find(class_ ='chalice-icon')
        if not t:
            title = heading_item.contents[0]
        else:
            title = heading_item.contents[1]

        url = body_item.find('a').attrs['href']


        URL_DICT[url] = title

    print('URL Dictionary Generated')
#init_category('/en-us/crownstore/eso-plus','s')

#exit(0)


#init()

for url, name in URL_DICT.items():
    init_category(url, name)