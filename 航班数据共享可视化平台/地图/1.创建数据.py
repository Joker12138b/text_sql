import pymysql

# 1.连接Mysql
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='98765', charset='utf8',db='unicom')
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)


# 2.发送指令(千万不要用字符串格式化做SQL的拼接，安全隐患SQL注入)
#下面的注释可用

# cursor.execute("insert into admin(username,password,mobile) values('dengwu','123456','10086')") #生成指令
# conn.commit()       #提交指令


# sa = "insert into admin(username,password,mobile) values(%s, %s, %s)"
# op = ['企业','wdwdwdwdwd','+0 123123']
# cursor.execute(sa, op) #生成指令,传列表形式
# conn.commit()       #提交指令


sa = "insert into admin(username,password,mobile) values(%(n1)s, %(n2)s, %(n3)s)"
op = {"n1":'贝尔法斯特', "n2":'164632165', "n3":'+0 wegqwef'}
cursor.execute(sa, op) #生成指令，传字典形式
conn.commit()       #提交指令

# 3.关闭连接
cursor.close()
conn.close()



