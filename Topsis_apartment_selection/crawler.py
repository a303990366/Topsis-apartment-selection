#from base import crawl_base
import re
import pandas as pd
import time
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
import math


class house_591:
    def __init__(self,county,town):
        super().__init__()
        self.town_df = pd.read_csv("./data/town.csv")#read county and town data
        self.url = None
        self.link_list = []
        self.county = county
        self.town = town
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}
        self.columns = ['title','role','user_id','traffic','life','education','price','price unit','rent type','area','building type','post time','update time','browse num',
                        'favorite num','equiment','fridge','washer','tv','cold','heater','bed','closet','fourth','net',
                        'gas','sofa','Chairs','balcony','lift','park','url'] #after equiment column,just raw data of equiment
        self.data_base = []
        self.driver = webdriver.Chrome(r"C:\Users\x5748\Downloads\chromedriver.exe")
    def create_query_url(self):
        
        town_query = '|'.join(self.town)#combine town info for query
        tmp = self.town_df[(self.town_df['county_label'].str.contains(self.county))&(self.town_df['label'].str.contains(town_query))]# query
        self.url = 'https://rent.591.com.tw/?region={0}&section={1}&searchtype=1'.format(tmp['county_value'].unique()[0],
                                                                                ','.join([str(i) for i in tmp['value'].values]))
    def get_item_number(self):
        '''choose county through selenium'''
        self.driver.get(self.url)     
        time.sleep(3)
        self.item_number = int(self.driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/section[2]/div/div/span').text)
    def crawl_link_list(self):
        '''get total links of item in a page'''
        item_list = self.driver.find_element_by_class_name('switch-list-content')
        item_list = item_list.find_elements_by_tag_name('section')
        self.link_list+=[i.find_element_by_tag_name('a').get_attribute('href') for i in item_list]#url
        print(len(self.link_list))
    def turn_page(self,total = None):
        '''turn page'''
        page_limit = test.driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/section[4]/div')
        if total == None:
            total = page_limit.find_element_by_class_name('pageNext').get_attribute('data-total')
            self.total = total
        self.driver.find_element_by_class_name("pageNext").click()
    def turn_and_crawl(self,times=None):
        '''combine crawl_link_list and turn_page funtions 
         variable:
             times-> type:int func: how many times we need to crawl'''
        if times ==None:
            time_all = math.ceil(self.item_number/30)-1
            for i in range(time_all):
                try:
                    self.crawl_link_list()
                    self.turn_page()
                    time.sleep(2)
                except Exception as e:
                    print(e)
                    self.driver.close()
        else:
            for i in range(times):
                self.crawl_link_list()
                self.turn_page()
                time.sleep(2)
        self.crawl_link_list()
        self.driver.close()
        
    def get_house_detail(self, house_id):
        """ detail of a item through link """
        # 紀錄 Cookie 取得 X-CSRF-TOKEN, deviceid
        s = requests.Session()
        url = f'https://rent.591.com.tw/home/{house_id}'
        r = s.get(url, headers=self.headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        token_item = soup.select_one('meta[name="csrf-token"]')

        headers = self.headers.copy()
        headers['X-CSRF-TOKEN'] = token_item.get('content')
        headers['deviceid'] = s.cookies.get_dict()['T591_TOKEN']
        # headers['token'] = s.cookies.get_dict()['PHPSESSID']
        headers['device'] = 'pc'

        url = f'https://bff.591.com.tw/v1/house/rent/detail?id={house_id}'
        r = s.get(url, headers=headers)
        if r.status_code != requests.codes.ok:
            print('請求失敗', r.status_code)
            return
        data = r.json()['data']
        title = data['title']
        role = data['linkInfo']['roleName'] #刊登人身分
        user_id = data['linkInfo']['uid'] #id
        map_data=data['positionRound']['mapData']#calc amount of store,school, and transportation near to the house
        each_field_num = []
        for cate in map_data:
            #print('field:',cate['name'])
            field_num=0
            for item in cate['children']:
                #print(item['name'],len(item))
                field_num+=len(item['children']) #!!!
            each_field_num.append(field_num)
        price = data['price']
        price_unit = data['priceUnit']#價格
        rent_type = data['info'][0]['value']#租屋的類型
        area = data['info'][1]['value']#坪數
        building_type = data['info'][-1]['value']#建築物類型
        post_time = data['publish']['postTime']#上架時間
        update_time = data['publish']['updateTime']#更新時間
        browse_num = data['browse']['pc']+data['browse']['mobile']#瀏覽數
        favorite_num = data['favData']['count']#收藏數
        equiment_data = data['service']['facility']
        equiment_active = [i['active'] for i in equiment_data]
        equiment_ratio = sum(equiment_active)/len(equiment_data)#設備完善率
        single_block = [title,role,user_id]+each_field_num 
        single_block += [price,price_unit,rent_type,area,building_type,post_time,update_time,browse_num,favorite_num,equiment_ratio]+equiment_active+[url]
        self.data_base.append(single_block)
        print('finish crawling one item')
        time.sleep(0.5)
        return data
    def output_frame(self):
        tmp = pd.DataFrame(self.data_base)
        tmp.columns=self.columns
        tmp.to_csv('./data/final_591data.csv',index = False)
    def main(self):
        count= 0
        self.create_query_url()
        self.get_item_number()
        self.turn_and_crawl()
        for link in self.link_list:
            pattern = '\d{4,8}'
            house_id = re.search(pattern,link).group()
            self.get_house_detail(int(house_id)) 
            count+=1
            
        #print('finsh all items({0})/{1}......'.format(len(self.data_base),self.total))
        print('finsh all items({0})......'.format(len(self.data_base)))
        self.output_frame()
if __name__ == '__main__':
    key_county = '花蓮' #要改
    key_town = ['吉安','花蓮'] #最多選3區
    test = house_591(key_county,key_town)
    test.main()
