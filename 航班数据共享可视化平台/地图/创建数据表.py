# conding=utf-8
import pymysql
import numpy as np
import pandas as pd
import re

from tqdm import trange


def table_exists(con, table_name):  # 这个函数用来判断表是否存在
    sql = "show tables;"
    con.execute(sql)
    tables = [con.fetchall()]
    table_list = re.findall('(\'.*?\')', str(tables))
    table_list = [re.sub("'", '', each) for each in table_list]
    if table_name in table_list:
        return 1  # 存在返回1
    else:
        return 0  # 不存在返回0


Depart_delay_time_all = pd.read_csv("static/airport/起飞机场不同时间延误时长.csv")
Arr_delay_time_all = pd.read_csv("static/airport/到达机场不同时间延误时长.csv")
Taxi_out_all = pd.read_csv("static/airport/机场不同时间推出时长.csv")
Taxi_in_all = pd.read_csv("static/airport/机场不同时间推入时长.csv")
Margins_all = pd.read_csv("static/airport/机场裕度.csv")
k_out_all = pd.read_csv("static/airport/机场出度.csv")
k_in_all = pd.read_csv("static/airport/机场入度.csv")

# 连接数据库 并添加cursor游标
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='98765', charset='utf8', db='airport_data')
cursor = conn.cursor()

for i in trange(k_in_all.shape[1] - 1):  # -1是因为unnamed：0行（机场索引行）要去除
    i = str(i)

    Depart_delay_time = Depart_delay_time_all.loc[:, [i]].values

    Arr_delay_time = Arr_delay_time_all.loc[:, [i]].values

    Taxi_out = Taxi_out_all.loc[:, [i]].values

    Taxi_in = Taxi_in_all.loc[:, [i]].values

    Margins = Margins_all.loc[:, [i]].values

    k_out = k_out_all.loc[:, [i]].values

    k_in = k_in_all.loc[:, [i]].values

    k_all = np.add(k_in, k_out)

    #  创建数据表的sql 语句  ，此处的`{}`是为了传入不同的数据表（time+i），无法避免SQL注入风险
    sql_createTb = """CREATE TABLE `{}` (
                     Airport INT,
                     Arr_delay_time FLOAT,
                     Depart_delay_time FLOAT,
                     Taxi_out FLOAT,
                     Taxi_in FLOAT,
                     Margins FLOAT,
                     k_in  INT,
                     k_out INT,
                     k_all INT,
                     DATA_Timing INT,
                     PRIMARY KEY(Airport))
                     """.format('time' + i)
    # 创建数据表
    if table_exists(cursor, 'time' + i) == 0:  # 判断是否已经有表Time5了，有了返回1,没有就跳过
        cursor.execute(sql_createTb)

    # 插入一条数据到数据表里面。
    sql_insert = "insert into `{}` (Airport,Depart_delay_time,Arr_delay_time,Taxi_out,Taxi_in,Margins,k_in,k_out,k_all,DATA_Timing)" \
                 "values(%(n1)s, %(n2)s, %(n3)s, %(n4)s, %(n5)s, %(n6)s, %(n7)s, %(n8)s, %(n9)s, %(n10)s)".format('time' + i)

    for j in range(len(k_all)):
        op = {"n1": j, "n2": Depart_delay_time[j].item(), "n3": Arr_delay_time[j].item(), "n4": Taxi_out[j].item(),
              "n5": Taxi_in[j].item(), "n6": Margins[j].item(),
              "n7": k_in[j].item(), "n8": k_out[j].item(), "n9": k_all[j].item(), "n10": int(i)}
        cursor.execute(sql_insert, op)  # 生成指令，传字典形式，op随便命名的变量
        conn.commit()
    # 在 execute里面执行SQL语句

conn.close()
cursor.close()
