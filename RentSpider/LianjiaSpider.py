from bs4 import BeautifulSoup
from SpiderBase import *
import re
import time
import csv


class RentInfo(object):
    def __init__(self):
        self.downtown = ''
        self.street = ''
        self.community = ''
        self.area = 0
        self.rent = 0
    

    def __repr__(self):
        return '%s, %s, %s, %d, %d' % (self.downtown, self.street, self.community, self.rent, self.area)


class LianjiaSpider(SpiderBase):
    def __init__(self):
        SpiderBase.__init__(self)
        self.rentMap = []


    def SaveData(self):
        if len(self.rentMap) == 0:
            return

        with open('data.csv', 'w', encoding='utf8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['downtown', 'street', 'community', 'rent', 'area'])
            for rentInfo in self.rentMap:
                csv_writer.writerow([rentInfo.downtown, rentInfo.street, rentInfo.community, str(rentInfo.rent), str(rentInfo.area)])


    def ParseInfo(self, houseInfo):
        res = houseInfo.find(class_='content__list--item--des').find_all('a')
        if res and len(res) == 3:
            rentInfo = RentInfo()
            rentInfo.downtown = res[0].text
            rentInfo.street = res[1].text
            rentInfo.community = res[2].text
            rentStr = houseInfo.find(class_ = 'content__list--item-price').find('em').text
            rentInfo.rent = int(rentStr)
            detail = houseInfo.find(class_='content__list--item--des').text 
            text = re.findall('(\d{1,}㎡)', detail)
            areaStr = text[0][0:-1]
            rentInfo.area = int(areaStr)
            self.rentMap.append(rentInfo)


    def HandleHtml(self, html):
        soup = BeautifulSoup(html, features='html.parser')
        houseList = soup.find(class_ = 'content__list').find_all(class_ = 'content__list--item--main')
        for houseInfo in houseList:
            self.ParseInfo(houseInfo)


    def Crawl(self):
        for index in range(1,100):
            url = 'https://hz.lianjia.com/zufang/pg%drco11/#contentList' % index
            if index == 1:
                url = 'https://hz.lianjia.com/zufang/rco11/#contentList'
            html = self.GetHtml(url)
            if html:
                self.HandleHtml(html)
            else:
                print(self.GetLastError())
            time.sleep(3)
        self.SaveData()
        