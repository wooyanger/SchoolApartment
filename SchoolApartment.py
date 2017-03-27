#!/usr/bin/python
# -*- encoding: utf-8 -*-

# Work on python 2.7
# Need requests bs4

from Mongo import Mongo
from requests import Session
from bs4 import BeautifulSoup

class SchoolApatment:
    __doc__ = '''这是一个基于 python 的爬虫，主要爬取省份，大学，大学学院及大学宿舍信息。并将信息
    保存至 MongoDB 中。'''

    def __init__(self):
        self.session = Session()
        self.m = Mongo('数据库连接', 27017, '数据库名称')

    # 大学信息
    def university(self):
        # 获取数据
        data = self.session.get('https://www.wooyang.ml/data/allunivlist.txt').content
        # 将str 转 list
        data = eval(data)
        for i in data:
            # 将数据存到对应collection 中
            self.m.insert(collection='country',data={'id': i['id'], 'country_name': i['name']})
            for j in i['univs']:
                self.m.insert(collection='university', data={'id': j['id'], 'university_name': j['name']})

    # 学院信息
    def college(self):
        # 从数据库中，取出需要的数据
        for university in self.m.find(collection='university'):
            college_list = []
            # 获取数据
            data = self.session.get(url='http://www.renren.com/GetDep.do?id=%d' % university['id'] )
            soup = BeautifulSoup(data.text, 'lxml')
            for j in soup.stripped_strings:
                if j.encode('utf-8') == '院系':
                    pass
                else:
                    college_list.append(j)
            self.m.insert(collection='college', data={'id': university['id'], 'college': college_list})

    # 宿舍信息
    def apartment(self):
        # 设置Cookie
        self.session.headers.update({'Cookie': 't=0e10866787e0a7fc1ac190a4d60c4f9e2'})
        for university in self.m.find(collection='university'):
            apartment_list = []
            data = self.session.post(url='http://www.renren.com/GetDorm.do', data={'id': university['id']} )
            soup = BeautifulSoup(data.text, 'lxml')
            for j in soup.stripped_strings:
                if j.encode('utf-8') == '宿舍':
                    pass
                else:
                    apartment_list.append(j)
            self.m.insert(collection='apartment', data={'id': university['id'], 'college': apartment_list})


    

if __name__ == '__main__':
    s = SchoolApatment()
    s.university()
    s.college()
    s.apartment()
