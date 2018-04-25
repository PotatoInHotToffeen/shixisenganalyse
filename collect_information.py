# -*- coding: UTF-8 -*-
import re
import requests
import MySQLdb
import time

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from cStringIO import StringIO
from fontTools.ttLib import TTFont

_pat_font_content = re.compile('myFont; src: url\("data:application/octet-stream;base64,(.+?)"')
_pat_font = re.compile('&#x[0-9a-f]{4}')

maps = {}


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    'Host': 'www.shixiseng.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
}


def get_font_regx(content):
    if content in maps:
        return maps[content]
    ctx = content.decode('base64')
    font = TTFont(StringIO(ctx))
    mappings = {}
    for k, v in font.getBestCmap().items():
        if v.startswith('uni'):
            mappings['&#x{:x}'.format(k)] = unichr(int(v[3:], 16))
        else:
            mappings['&#x{:x}'.format(k)] = v

    def callback(regx):
        return mappings.get(regx.group(0), regx.group(0))
    maps[content] = callback
    return callback

# def open_database():
#     conn = MySQLdb.connect(host="localhost", user="root", passwd="luckyyuee", db="shixiseng", charset="utf8")
#     cursor = conn.cursor()


if __name__ == '__main__':
    #打开数据库
    conn = MySQLdb.connect(host='localhost',port=3306,user='root',passwd='1234567',db='shixiseng',charset="utf8")
    cursor = conn.cursor()

    basic_web='https://www.shixiseng.com/sheji/'
    for i in range(1,501):
        detail_web=basic_web+str(i);
        resp = requests.get(detail_web, headers=headers)
        resp.encoding = "utf-8"
        content = _pat_font_content.search(resp.text).group(1)
        callback = get_font_regx(content)
        text = _pat_font.sub(callback, resp.text)
        pattern = re.compile(
            r'<li class="font">.*?data-info="inn_(.*?)".*?data-sname="95".*?>(.*?)</a>.*?data-sname="96".*?>(.*?)</a>.*?<span class="type">(.*?)</span>.*?<div class="area">(.*?)</div>.*?<div class="more">.*?<span>'
            r'(.*?)-(.*?)/.*?</span>.*?<span>(.*?)</span>.*?<span>(.*?)</span>'
            ,re.S)
        items = re.findall(pattern, text)
    # Basic_infor=[]
    # sql = "insert into basic_infor values"
    #     r1 = u"[—·']+"
        for item in items:
            idd=item[0]
            intership=re.sub("'", r"\'", item[1])
            company=re.sub("'", r"\'", item[2])
                # re.sub(r1, '-',item[2] )
            catecoriy=item[3]
            d_salary_down=int(item[5])
            d_salary_up=int(item[6])
            d_salary_average=((d_salary_down+d_salary_up)/2.0)
            week_workday = int(re.sub(r'\D', "", item[7]))
            month_NTD=int(re.sub(r'\D', "", item[8]))
            # print company
        # print intership,company,catecoriy,country,d_salary_down,d_salary_up,d_salary_average,week_workday,month_NTD
            country_list=item[4].split(',')
            country_list_len=len(country_list)
            for ii in range(0,country_list_len):
                country=country_list[ii]
                real_idd=idd
                if(country_list_len>1):
                    real_idd=idd+str(ii);
                sql ="insert into basic_infor values('%s','%s','%s','%s','%s',%s,%s,%s,%s,%s,null)" % (real_idd,intership,company,catecoriy,country,d_salary_down,d_salary_up,d_salary_average, week_workday,month_NTD)
        # print sql
                cursor.execute(sql)
                conn.commit()
        print"第%s页读取完毕"%(i)
        time.sleep(1);
        # Basic_infor.append([item[0],item[1],item[2],item[3],int(item[4]),int(item[5]),d_salary_average,int(week_workday),int(month_NTD)])
        # print item[0],item[1],item[2],item[3],item[4],item[5],d_salary_average,week_workday,month_NTD+'\n'
        # print item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7]
    # print(text)
    # print Basic_infor
    print "全部读取完毕"
    # conn.executemany(sql, Basic_infor)
    # conn.commit()
    cursor.close()
    conn.close()