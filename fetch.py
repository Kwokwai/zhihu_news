#-*- coding:utf-8 -*-

from Zh_news.settings import DATABASES
from bs4 import BeautifulSoup
from collections import OrderedDict
from colorama import init, Fore
import urllib
import urllib2
import requests
import MySQLdb
import time


def get_news(mysql, news_list_table, referer_url):
    news_list = OrderedDict()

    html = 'http://daily.zhihu.com/'
    requests = urllib2.Request(html, headers={'referer': referer_url}) #referer解决图片外链显示不了的问题
    response = urllib2.urlopen(requests)
    get_html = response.read().decode('utf8')
    soup = BeautifulSoup(get_html, 'html.parser')
    items = soup.find_all('div', 'box')

    for item in items:
        image = item.img['src']
        title = item.span.get_text()
        id = item.a['href'].split('/')[2]
        url = html + 'story/' + id
        image_name = image.split('/')[-1]


        news_list['news_id'] = id
        news_list['news_title'] = title
        news_list['image_url'] = image
        news_list['share_url'] = url

        print Fore.YELLOW + "----------开始插入数据----------"
        for key, values in news_list.items():
            print key + ':' + values

        result = mysql.insert_data(news_list_table, news_list)
        if result:
            print Fore.GREEN + "news_list_talle:数据保存成功!"


class Mysql(object):
    def get_current_time(self):
        created_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return created_time

    def __init__(self, host, user, passwd, db, port):
        try:
            self.db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, port=port, charset='utf8')
            self.cur = self.db.cursor()
        except MySQLdb.Error as e:
            print Fore.RED + '连接数据库失败'
            print Fore.RED + self.get_current_time(), '[%Y-%m-%d %H:%M:%S]', time.localtime(time.time())

    def insert_data(self, table, my_dict):
        try:
            cols = ','.join(my_dict.keys())
            values = '","'.join(my_dict.values())
            values = '"' + values + '"'
            try:
                sql = "insert into %s (%s) values(%s)" % (table, cols, values)
                self.cur.execute(sql)
                self.db.commit()
                return 1
            except MySQLdb.Error as e:
                self.db.rollback()
                if "key 'PRIMARY'" in e.args[1]:
                    print Fore.RED + self.get_current_time() + "  数据已存在，未插入数据,更新时间戳："
                    result = self.update_timestamp(table, my_dict)
                    if result:
                        print Fore.GREEN + "%s: 更新时间戳成功！" % table
                    else:
                        print Fore.GREEN + "%s: 更新时间戳失败！" % table
                    return 0
                else:
                    print Fore.RED + self.get_current_time(), "插入数据失败，原因 %d: %s" % (e.args[0], e.args[1])
                return 0
        except MySQLdb.Error as e:
            print Fore.RED + self.get_current_time(), "数据库错误，原因%d: %s" % (e.args[0], e.args[1])
            return 0

    def update_timestamp(self, table, my_dict):
        title_field = my_dict.keys()[1]
        title_field_values = my_dict.values()[1]
        datetime = self.get_current_time()
        sql = "update %s set created='%s' where %s='%s' " % (table, datetime, title_field, title_field_values)
        # print "sql:",sql
        self.cur.execute(sql)
        self.db.commit()
        return 1

    def close_connect(self):
        self.cur.close()
        self.db.close()


if __name__ == '__main__':
    host = DATABASES['default']['HOST']
    user = DATABASES['default']['USER']
    passwd = DATABASES['default']['PASSWORD']
    db = DATABASES['default']['NAME']
    port = DATABASES['default']['PORT']

    news_list_table = 'news_news'
    init(autoreset=True)
    referer_url = 'http://daily.zhihu.com/'

    mysql = Mysql(host, user, passwd, db, port)
    get_news(mysql, news_list_table, referer_url)
    mysql.close_connect()