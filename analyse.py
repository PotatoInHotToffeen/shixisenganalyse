# -*- coding: UTF-8 -*-
import resultshow
import MySQLdb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import jieba
from wordcloud import WordCloud
import jieba.analyse
import random
import os
import codecs
from scipy.misc import imread

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def test(text):
    #设置seaborn的style
    sns.set(style="darkgrid", palette="muted", color_codes=True)

    #字体赋值设置
    YAHEI = matplotlib.font_manager.FontProperties(fname="Microsoft YaHei UI.ttc")
    KAITI=  matplotlib.font_manager.FontProperties(fname="AdobeKaitiStd-Regular.otf")
    CALIBRI=matplotlib.font_manager.FontProperties(fname="calibri.ttf")

    #matplotlib字体默认设置为仿宋
    plt.rcParams['font.sans-serif']=['FangSong']
    plt.rcParams['axes.unicode_minus'] = False

    #连接数据库并获取数据放置在df里
    conn = MySQLdb.connect(host='localhost',port=3306,user='root',passwd='1234567',db='shixiseng',charset="utf8")
    df = pd.read_sql("select * from full_infor",con=conn)
    conn.close()

    #对数据进行清洗
    def random_type(text):
        typelist=text.split(",")
        typenumber=len(typelist)
        return typelist[random.randint(0,typenumber-1)]

    df=df.drop_duplicates(subset='job_key',keep='first')  #筛选掉重复的数据
    df=df.drop('city', axis=1).join(df['city'].str.split(',', expand=True).stack().reset_index(level=1, drop=True).rename('city')) #将列为“城市”的行按照逗号分开

    if text!='':
        df[df.intership.contains(text)]
    df=df[ df['city'] !='']  #去除分行后city为空的数据
    df=df[ df['city'] !=u'全国'] #去除city为“全国”的数据
    df=df[df['d_salary_up']<450] #去除日工资过高怀疑是月工资的数据
    df['typeofcompany']= df.apply(lambda x:random_type(x.typeofcompany),axis=1)#公司类型多于2个的选取其一作为唯一类型

    #top_city是排名最前10的城市
    top_city=df['city'].value_counts().reset_index()[:10]
    #city&出现数量(降序、全部城市) dataframe类型
    city_counts=df['city'].value_counts().reset_index()

    #十大城市职位柱状图
    f, ax= plt.subplots(figsize = (8, 6))
    ax.set_title(u'发布实习生职位最多的十个城市',fontsize=22,fontproperties=KAITI)
    ax.tick_params(axis='x',labelsize=12)
    ax.tick_params(axis='y',labelsize=12)
    sns.countplot(x='city',data =df,order=df.city.value_counts().iloc[:10].index)
    ax.set_xlabel(u'城市',fontsize=12,fontproperties=KAITI)
    ax.set_ylabel(u'岗位数量',fontsize=12,fontproperties=KAITI)
    for a,b in zip(range(0,10),top_city['city']):
        plt.text(a, b, b, ha='center', va= 'bottom',fontsize=11,fontproperties=CALIBRI)
    f.savefig("analysephoto/1.png")

    tencitylist=df.city.value_counts().iloc[:10].index
    tencitycount=df['city'].value_counts().reset_index()[:10].city
    str=''
    for i in range(0,10):
        str+=tencitylist[i]+u"、"
    str=str[:-1]
    analysetext=u'发布职位最多的十个城市分别为'+str+u'；其中'+tencitylist[0]+u"以"+bytes(tencitycount[0])+u"个职位位居榜首。"
    f=open('analysephoto/1.txt','w')
    f.write(analysetext)
    f.close()

    #最多职位的十个工作类型是
    f, ax= plt.subplots(figsize = (8, 6))
    ax.set_title(u'发布职位最多的十个工作类型',fontsize=22,fontproperties=KAITI)
    ax.tick_params(axis='x',labelsize=12)
    ax.tick_params(axis='y',labelsize=12)
    sns.countplot(x='categoriy',data =df,order=df.categoriy.value_counts().iloc[:10].index)
    ax.set_xlabel(u'工作类型',fontsize=12,fontproperties=KAITI)
    ax.set_ylabel(u'岗位数量',fontsize=12,fontproperties=KAITI)
    for a,b in zip(range(0,10),df['categoriy'].value_counts().reset_index()[:10]['categoriy']):
        plt.text(a, b, b, ha='center', va= 'bottom',fontsize=11,fontproperties=CALIBRI)
    f.savefig("analysephoto/2.png")

    tencategoriylist=df.categoriy.value_counts().iloc[:10].index
    str=''
    for i in range(0,10):
        str+=tencategoriylist[i]+u"、"
    str=str[:-1]
    analysetext=u'发布职位最多的十个工作类型为'+str+u'；'+tencategoriylist[0]+u"类型的工作发布得最多，最需要实习生。"
    f=open('analysephoto/2.txt','w')
    f.write(analysetext)
    f.close()

    #全国工资分布直方图
    df['d_salary_average']= df.apply(lambda x:(x.d_salary_down+x.d_salary_up)/2,axis=1)
    f, ax= plt.subplots(figsize = (8, 6))
    ax.set_title(u'工资分布',fontsize=22,fontproperties=KAITI)
    sns.distplot(df['d_salary_average'] ,bins=int(400/50),kde=False,label=u'日工资')
    ax.set_xlabel(u'日工资（单位：元）',fontsize=12,fontproperties=KAITI)
    ax.set_ylabel(u'分布数量',fontsize=12,fontproperties=KAITI)
    for a,b in zip(range(25,400,50),pd.cut(df['d_salary_average'], 8).value_counts(sort=False).reset_index()['d_salary_average']):
        plt.text(a, b, b, ha='center', va= 'bottom',fontsize=11,fontproperties=CALIBRI)
    f.savefig("analysephoto/3.png")

    d_salary_list=pd.cut(df['d_salary_average'], 8).value_counts(sort=True).reset_index()
    analysetext=u"平均日工资大部分分布在100.75~150.625元,其次为50.875~100.75元。"
    f=open('analysephoto/3.txt','w')
    f.write(analysetext)
    f.close()

    #工作天数要求柱状图
    f, ax= plt.subplots(figsize = (8, 6))
    ax.set_title(u'工作天数要求分布',fontsize=22,fontproperties=KAITI)
    ax.tick_params(axis='x',labelsize=12)
    ax.tick_params(axis='y',labelsize=12)
    sns.countplot(x='workday',data =df,order=df.workday.value_counts(sort=False).index)
    ax.set_xlabel(u'工作天数',fontsize=12,fontproperties=KAITI)
    ax.set_ylabel(u'岗位数量',fontsize=12,fontproperties=KAITI)
    for a,b in zip(range(0,7),df['workday'].value_counts(sort=False).reset_index()['workday']):
        plt.text(a, b, b, ha='center', va= 'bottom',fontsize=11,fontproperties=CALIBRI)
    f.savefig("analysephoto/4.png")

    tenworkdaylist=df.workday.value_counts().iloc[:10].index
    tenworkdaycount=df['workday'].value_counts().reset_index()[:10].workday
    analysetext='%.2f%%' % (tenworkdaycount[0]*1.0/len(df) * 100)+u"职位都需要每周工作"+bytes(tenworkdaylist[0])+u"天，其次为"+bytes(tenworkdaylist[1])+u"天,占比为"+'%.2f%%' % (tenworkdaycount[1]*1.0/len(df) * 100)
    f=open('analysephoto/4.txt','w')
    f.write(analysetext)
    f.close()

    #工作月份要求柱状图
    f, ax= plt.subplots(figsize = (8, 6))
    ax.set_title(u'工作月份要求分布(前6名)',fontsize=22,fontproperties=KAITI)
    ax.tick_params(axis='x',labelsize=12)
    ax.tick_params(axis='y',labelsize=12)
    sns.countplot(x='month',data =df,order=df.month.value_counts().iloc[:6].index)
    ax.set_xlabel(u'工作月份',fontsize=12,fontproperties=KAITI)
    ax.set_ylabel(u'岗位数量',fontsize=12,fontproperties=KAITI)
    for a,b in zip(range(0,6),df['month'].value_counts().reset_index()[:6]['month']):
        plt.text(a, b, b, ha='center', va= 'bottom',fontsize=11,fontproperties=CALIBRI)
    f.savefig("analysephoto/5.png")

    tenworkdaylist=df.workday.value_counts().iloc[:10].index
    tenworkdaycount=df['workday'].value_counts().reset_index()[:10].workday
    analysetext='%.2f%%' % (tenworkdaycount[0]*1.0/len(df) * 100)+u"职位都需要每周工作"+bytes(tenworkdaylist[0])+u"天，其次为"+bytes(tenworkdaylist[1])+u"天,占比为"+'%.2f%%' % (tenworkdaycount[1]*1.0/len(df) * 100)
    f=open('analysephoto/5.txt','w')
    f.write(analysetext)
    f.close()

    #学历要求柱状图
    f, ax= plt.subplots(figsize = (8, 6))
    ax.set_title(u'学历要求分布',fontsize=22,fontproperties=KAITI)
    ax.tick_params(axis='x',labelsize=12)
    ax.tick_params(axis='y',labelsize=12)
    sns.countplot(x='degree',data =df,order=df.degree.value_counts().index)
    ax.set_xlabel(u'学历要求',fontsize=12,fontproperties=KAITI)
    ax.set_ylabel(u'岗位数量',fontsize=12,fontproperties=KAITI)
    for a,b in zip(range(0,4),df['degree'].value_counts().reset_index()['degree']):
        plt.text(a, b, b, ha='center', va= 'bottom',fontsize=11,fontproperties=CALIBRI)
    f.savefig("analysephoto/6.png")

    tenworkdaylist=df.workday.value_counts().iloc[:10].index
    tenworkdaycount=df['workday'].value_counts().reset_index()[:10].workday
    analysetext='%.2f%%' % (tenworkdaycount[0]*1.0/len(df) * 100)+u"职位都需要每周工作"+bytes(tenworkdaylist[0])+u"天，其次为"+bytes(tenworkdaylist[1])+u"天,占比为"+'%.2f%%' % (tenworkdaycount[1]*1.0/len(df) * 100)
    f=open('analysephoto/6.txt','w')
    f.write(analysetext)
    f.close()

    #公司类型最多的为何类型
    f, ax= plt.subplots(figsize = (8, 6))
    ax.set_title(u'发布实习生职位最多的十个公司类型',fontsize=22,fontproperties=KAITI)
    ax.tick_params(axis='x',labelsize=12)
    ax.tick_params(axis='y',labelsize=12)
    sns.countplot(x='typeofcompany',data =df,order=df.typeofcompany.value_counts().iloc[:6].index)
    ax.set_xlabel(u'公司类型',fontsize=12,fontproperties=KAITI)
    ax.set_ylabel(u'岗位数量',fontsize=12,fontproperties=KAITI)
    for a,b in zip(range(0,10),df['typeofcompany'].value_counts().reset_index()[:6]['typeofcompany']):
        plt.text(a, b, b, ha='center', va= 'bottom',fontsize=11,fontproperties=CALIBRI)
    f.savefig("analysephoto/7.png")

    tenworkdaylist=df.workday.value_counts().iloc[:10].index
    tenworkdaycount=df['workday'].value_counts().reset_index()[:10].workday
    analysetext='%.2f%%' % (tenworkdaycount[0]*1.0/len(df) * 100)+u"职位都需要每周工作"+bytes(tenworkdaylist[0])+u"天，其次为"+bytes(tenworkdaylist[1])+u"天,占比为"+'%.2f%%' % (tenworkdaycount[1]*1.0/len(df) * 100)
    f=open('analysephoto/7.txt','w')
    f.write(analysetext)
    f.close()

    #不同城市对薪资的影响
    f, ax= plt.subplots(figsize = (8, 6))
    ax.set_title(u'不同城市对薪资的影响(箱线图)',fontsize=22,fontproperties=KAITI)
    ax.tick_params(axis='x',labelsize=12)
    ax.tick_params(axis='y',labelsize=12)
    sns.boxplot(x='city',y='d_salary_average',data=df,order=df.city.value_counts().iloc[:10].index);
    ax.set_xlabel(u'城市',fontsize=12,fontproperties=KAITI)
    ax.set_ylabel(u'薪资',fontsize=12,fontproperties=KAITI)
    f.savefig("analysephoto/8.png")

    tenworkdaylist=df.workday.value_counts().iloc[:10].index
    tenworkdaycount=df['workday'].value_counts().reset_index()[:10].workday
    analysetext='%.2f%%' % (tenworkdaycount[0]*1.0/len(df) * 100)+u"职位都需要每周工作"+bytes(tenworkdaylist[0])+u"天，其次为"+bytes(tenworkdaylist[1])+u"天,占比为"+'%.2f%%' % (tenworkdaycount[1]*1.0/len(df) * 100)
    f=open('analysephoto/8.txt','w')
    f.write(analysetext)
    f.close()

    #不同学历对薪资的影响
    f, ax= plt.subplots(figsize = (8, 6))
    ax.set_title(u'不同学历对薪资的影响(箱线图)',fontsize=22,fontproperties=KAITI)
    ax.tick_params(axis='x',labelsize=12)
    ax.tick_params(axis='y',labelsize=12)
    sns.boxplot(x='degree',y='d_salary_average',data=df,order=df.degree.value_counts().iloc[:10].index);
    ax.set_xlabel(u'学历',fontsize=12,fontproperties=KAITI)
    ax.set_ylabel(u'薪资',fontsize=12,fontproperties=KAITI)
    f.savefig("analysephoto/9.png")

    tenworkdaylist=df.workday.value_counts().iloc[:10].index
    tenworkdaycount=df['workday'].value_counts().reset_index()[:10].workday
    analysetext='%.2f%%' % (tenworkdaycount[0]*1.0/len(df) * 100)+u"职位都需要每周工作"+bytes(tenworkdaylist[0])+u"天，其次为"+bytes(tenworkdaylist[1])+u"天,占比为"+'%.2f%%' % (tenworkdaycount[1]*1.0/len(df) * 100)
    f=open('analysephoto/9.txt','w')
    f.write(analysetext)
    f.close()

    #词云jieba、词典设置
    jieba.load_userdict('userdict.txt')
    jieba.analyse.set_stop_words('STOPWORD.txt')

    def key_words(text):
        key_words=jieba.analyse.extract_tags(text,topK=50,withWeight=False,allowPOS=())
        return key_words

    def write_to_text(word_list):
        f=open('word_list_text.txt','a')
        for word in word_list:
            f.writelines((word+u',').encode('utf-8'))
        f.close()

    #职业诱惑关键字
    keyword_careertemp=df['carerr_tempation'].apply(key_words)
    f=open('word_list_text.txt','w')
    f.close()
    keyword_careertemp.apply(write_to_text)
    text=open('word_list_text.txt','r').read()
    text=unicode(text,encoding='utf-8')

    wcd=WordCloud(font_path='simsun.ttc',width=900,height=400,background_color='white',collocations=False).generate(text)
    wcd.to_file('analysephoto/10.png')

    tenworkdaylist=df.workday.value_counts().iloc[:10].index
    tenworkdaycount=df['workday'].value_counts().reset_index()[:10].workday
    analysetext='%.2f%%' % (tenworkdaycount[0]*1.0/len(df) * 100)+u"职位都需要每周工作"+bytes(tenworkdaylist[0])+u"天，其次为"+bytes(tenworkdaylist[1])+u"天,占比为"+'%.2f%%' % (tenworkdaycount[1]*1.0/len(df) * 100)
    f=open('analysephoto/10.txt','w')
    f.write(analysetext)
    f.close()

    # resultshow.show()

    # #城市发布职位数量饼图
    # df['city'].loc[~df['city'].isin(top_city['index'])]=u"其他城市"
    # city_counts=df['city'].value_counts().reset_index()
    # f, ax= plt.subplots(figsize = (8, 6))
    # ax.set_title(u'城市发布职位占比百分数',fontsize=22,fontproperties=KAITI)
    # explode = [0.1,0,0,0,0,0,0,0.1,0.1,0.2,0.1]
    # ax.pie(city_counts['city'],explode=explode,pctdistance=0.7,labels=city_counts['index'], autopct='%1.1f%%', startangle=90,shadow=True,textprops={'fontsize':9,'fontproperties':YAHEI})
    # ax.axis('equal')
    # # plt.show()
    #
    #
    # # print df.groupby(['city']).size().plot.pie(figsize=(6,6))
    # # plt.show()
    # # ['Id'].count().plot.pie(figsize=(6,6))

    #
    #
    # #学历要求柱饼状图
    # f, ax= plt.subplots(figsize = (8, 6))
    # ax.set_title(u'学历要求占比百分数',fontsize=22,fontproperties=KAITI)
    # explode = [0,0,0,0.1]
    # ax.pie(df['degree'].value_counts().reset_index()['degree'],explode =explode,pctdistance=0.7,labels=df['degree'].value_counts().reset_index()['index'],autopct='%1.1f%%', startangle=90,shadow=True,textprops={'fontsize':9,'fontproperties':YAHEI})
    # ax.axis('equal')
    #
    #
    # #实习月份要求饼状图
    # f4, ax= plt.subplots(figsize = (8, 6))
    # ax.set_title(u'实习月份占比百分数',fontsize=22,fontproperties=KAITI)
    # ax.pie(df['month'].value_counts().reset_index()['month'],pctdistance=0.7,labels=df['month'].value_counts().reset_index()['index'],autopct='%1.1f%%', startangle=90,shadow=True,textprops={'fontsize':9,'fontproperties':YAHEI})
    # ax.axis('equal')
    #
    # #公司规模要求柱状图
    # f1, ax= plt.subplots(figsize = (8, 6))
    # ax.set_title(u'要求实习月份最多的十个月份',fontsize=22,fontproperties=KAITI)
    # # ax.set_xlabel('X Label',fontsize=10)
    # ax.tick_params(axis='x',labelsize=6)
    # ax.tick_params(axis='y',labelsize=12)
    # sns.countplot(x='size',data =df,order=df["size"].value_counts().index)
    # # print a.get_x()
    # ax.set_xlabel(u'公司规模',fontsize=12,fontproperties=KAITI)
    #               # rotation='horizontal',labelpad = 12.5)
    # ax.set_ylabel(u'岗位数量',fontsize=12,fontproperties=KAITI)
    # for a,b in zip(range(0,15),df['size'].value_counts().reset_index()['size']):
    #     plt.text(a, b, b, ha='center', va= 'bottom',fontsize=11,fontproperties=CALIBRI)
    #
    #

    # def grey_color_func(word,font_size,position,orientation,random_state=None,**kwargs):
    #     return "hsl(0,0%%,%d%%)"%random.randint(0,10)

    # fig=plt.figure(figsize=(9,4))
    # # f,axs=plt.subplots(figsize=(15,15))
    # # wcd.fit_words(text)
    # # axs=plt.imshow(wcd)
    # plt.imshow(wcd)
    # plt.axis("off")

    # plt.show()
    # #职业诱惑关键字
    # keyword_description=df['description'].apply(key_words)
    # f=open('word_list_text.txt','w')
    # f.close()
    # keyword_description.apply(write_to_text)
    # # print df['key_words']
    # text=open('word_list_text.txt','r').read()
    # text=unicode(text,encoding='utf-8')
    #
    # wcd=WordCloud(font_path='simsun.ttc',width=900,height=400,background_color='white').generate(text)
    # wcd.to_file('3.jpg')

