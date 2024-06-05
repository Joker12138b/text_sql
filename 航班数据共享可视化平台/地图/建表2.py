# conding=utf-8
import pymysql
import numpy as np
import pandas as pd
import re
import pandas as pd



#读取csv文件
df = pd.read_csv('static/airline/中国内地航司航班执行取消率同比数据列表.csv',encoding='utf8')
#连接MySQL数据库
db = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='98765', charset='utf8', db='airline_data')
#创建游标对象
cursor = db.cursor()
#创建表
cursor.execute("""
CREATE TABLE IF not Exists airline(
    id INT,
    airline VARCHAR(255) NOT NULL,
    date Date,
    flight_plan_number INT,
    flight_execution_number INT,
    flight_cancellation_number INT,
    cancellation_rate VARCHAR(255) NOT NULL
    )
    DEFAULT CHARSET=utf8;""")

#将数据库写入MySQL表
for index,row in df.iterrows():# 输出每行的索引值
    sql = 'INSERT INTO airline (id,airline,date,flight_plan_number,flight_execution_number,flight_cancellation_number,cancellation_rate) VALUES (%s, %s, %s, %s, %s, %s, %s)'
    values = (row['id'],row['airline'],row['date'],row['flight_plan_number'],row['flight_execution_number'],row['flight_cancellation_number'],row['cancellation_rate'])
    # print("插入数据成功")
    cursor.execute(sql,values)

    print(values)

#提交更改
db.commit()
cursor.close()
db.close()
