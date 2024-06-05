import pymysql
import asyncio
import websockets
import pymysql
import json



#打开数据库连接
db = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='98765', charset='utf8',db='airline_data')
#使用cursor()方法获取操作游标 
cursor = db.cursor()
#sql语句
sql = "select * from airline"

cursor.execute(sql)  # 生成指令,第二个参数对应上一行里的%s,也可以是多个的列表形式[1,3,4]
air_ = cursor.fetchall() # 获取mysql传输的值
air_line = []
# a = input("需要的时间区间，空格区分：").split()
# a_start = int(a[0])
# a_end = int(a[-1])

for i in range(0,50):
    air_line.append(air_[i])

airline = {
    "id": [item[0] for item in air_line],
    "airline": [item[1] for item in air_line],
    "date":[[item[2].year, item[2].month, item[2].day] for item in air_line],
    "flight_plan_number":[item[3] for item in air_line],
    "flight_execution_number":[item[4] for item in air_line],
    "flight_cancellation_number":[item[5] for item in air_line],
    "cancellation_rate":[item[6] for item in air_line]
}
data_json = json.dumps(airline)
print(data_json)
async def handle_websocket(websocket, path):
    while True:
        # 添加5秒的等待时间
        await asyncio.sleep(1)
        # 发送 JSON 数据到客户端
        await websocket.send(data_json)

# 创建WebSocket服务器，监听在指定的主机和端口
start_server = websockets.serve(handle_websocket, "localhost", 8769)

# 启动WebSocket服务器
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
