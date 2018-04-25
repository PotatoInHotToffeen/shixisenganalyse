# -*- coding: UTF-8 -*-
import MySQLdb
import pandas as pd
import numpy as np
import MySQLdb

#获取数据(脏数据)
conn = MySQLdb.connect(host='localhost',port=3306,user='root',passwd='1234567',db='shixiseng',charset="utf8")
df = pd.read_sql("select * from new_collect",con=conn)
conn.close()

#删除重复数据(根据job_key来确定是否重复)
if (len(df.job_key.unique()<len(df))):
    df=df.drop_duplicates(subset='job_key',keep='first')
# print df

#city字段可能有多个城市，需要分开各个城市并重新插入，注意key也需要变动

# df.replace(r'\，| ',np.nan,regex=True)
# print(df.loc[df["job_key"] == "w4huek4noqiy"].head())

#按照半角逗号分开并删除空字符串及空值的行
df=df.drop('city', axis=1).join(df['city'].str.split(',', expand=True).stack().reset_index(level=1, drop=True).rename('city')) #暂时没有变动key
# df=df.dropna(axis=0,how='any')
df=df[ df['city'] !='']
# print df
# print df.city.value_counts()
#d_salary需要分成两个字段，都为int类型，日工资上限及下限
df['d_salary_down'], df['d_salary_up'] = df['d_salary'].str.split('-', 1).str
df['d_salary_down']=df['d_salary_down'].astype(int)
df['d_salary_up']=df['d_salary_up'].astype(int)
print df
#将week_workday改成int类型，不包含“/周”字段，只包含数字

#将month_NTD改成int类型，不包含“/月”字段，只包含数字

#将
