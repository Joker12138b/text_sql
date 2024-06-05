import asyncio
import websockets
import numpy as np
import pandas as pd
import random
import pymysql
import json
import re

print("waiting...")

# 自定义排序函数，按time后面的值进行排序
# 自定义排序函数，使用正则表达式提取时间后面的值进行排序
def sort_key(table_name):
    match = re.match(r'time(\d+)', table_name)
    if match:
        return int(match.group(1))
    return 0


airport_all = pd.read_csv("static/airport/机场代码转换编号_带坐标.csv")
lon_lat = []
for _, row in airport_all.iterrows():
    values = [row["0"], row["Unnamed: 2"], -row["经度（W）"], row["纬度（N）"]]
    lon_lat.append(values)

Degree_Centrality = pd.read_csv("static/airport/度中心性.csv").values
Degree_Centrality = [[int(row[0]), round(row[1], 4)] for row in Degree_Centrality]

Feature_Centrality = pd.read_csv("static/airport/特征向量中心性.csv").values
Feature_Centrality = [[int(row[0]), round(row[1], 4)] for row in Feature_Centrality]

print("connecting mysql")
# 1.连接Mysql
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='98765', charset='utf8',db='airport_data')
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

# # 3.关闭连接
# cursor.close()
# conn.close()


print("start")
is_debug = int(input("是否为调试模式,1为调试，0为运行:"))
# 定义一个函数，用于处理WebSocket连接
async def handle_websocket(websocket, path):
    while True:
        data_h = []
        if is_debug:
            a = input("需要的时间区间，空格区分：").split()
            a_start = int(a[0])
            a_end = int(a[-1])
            for i in range(a_start, a_end):
                # 2.发送指令(千万不要用字符串格式化做SQL的拼接，安全隐患SQL注入)
                sa = "select * from {}".format('time' + str(i))  # 此处就是用mysql的查询语句
                cursor.execute(sa)  # 生成指令,第二个参数对应上一行里的%s,也可以是多个的列表形式[1,3,4]
                all_info = cursor.fetchall()  # 获取mysql传输的值       #fetchone()只获取筛选出的第一条数据
                data_h.append(all_info)

        else:
            # 查询最新的以"time"开头的表名
            cursor.execute("SHOW TABLES LIKE 'time%'")
            table_names = cursor.fetchall()
            # 提取所有字典的值
            all_values = []
            for dictionary in table_names:
                for value in dictionary.values():
                    all_values.append(value)
            # 获取最后的24个表，根据time后面的值排序
            last_24_table_names = sorted(all_values, key=sort_key)[-24:]
            # 查询这些表的数据
            for table_name in last_24_table_names:
                cursor.execute(f"SELECT * FROM {table_name}")
                all_info = cursor.fetchall()
                data_h.append(all_info)


        data_to_send = {
            "lon_lat": lon_lat,
            "Degree_Centrality": Degree_Centrality,
            "Feature_Centrality": Feature_Centrality,
            "data_h": data_h,
        }
        # 将字典转换为 JSON 格式
        data_json = json.dumps(data_to_send)
        # 添加5秒的等待时间
        await asyncio.sleep(5)
        # 发送 JSON 数据到客户端
        await websocket.send(data_json)



# 创建WebSocket服务器，监听在指定的主机和端口
start_server = websockets.serve(handle_websocket, "localhost", 8765)

# 启动WebSocket服务器
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
