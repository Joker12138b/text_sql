import pymysql

# 1.连接Mysql
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='98765', charset='utf8',db='unicom')
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)


# 2.发送指令(千万不要用字符串格式化做SQL的拼接，安全隐患SQL注入)
sa = "update admin set mobile=%s where id = %s"  #此处就是用mysql的查询语句
cursor.execute(sa, [258753, 3])#生成指令,第二个参数对应上一行里的%s,也可以是多个的列表形式[1,3,4]
conn.commit()

sa = "select * from admin"  #此处就是用mysql的查询语句
cursor.execute(sa)#生成指令,第二个参数对应上一行里的%s,也可以是多个的列表形式[1,3,4]
datalist = cursor.fetchall() #获取mysql传输的值       #fetchone()只获取筛选出的第一条数据
print(datalist)

# 3.关闭连接
cursor.close()
conn.close()
