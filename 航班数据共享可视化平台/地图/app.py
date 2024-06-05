# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify,url_for,redirect, flash
from flask_restful import Resource, Api, reqparse
import pymysql
import matplotlib.pyplot as plt
import io
import numpy as np
import mysql.connector
import base64
import json


app = Flask(__name__)
api = Api(app)
app.secret_key = 'your_secret_key'  # 设置一个密钥，用于 session 加密

db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '0000',
    'database': 'plot'
}

# 连接数据库
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

@app.route('/')
def sign_in_():
    return render_template("sign-in.html")#sign-in

@app.route('/add/user',methods=["GET","POST"])
def add_user():
    if request.method == "GET":
        return render_template("add_user.html")
    # print(request.form)
    username = request.form.get("user")
    password = request.form.get("pwd")
    #连接MySQL
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='98765', charset='utf8', db='unicom')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    #发送指令执行sql
    sql = "insert into admin1(username,password) values(%s,%s)"
    cursor.execute(sql,[username,password])  # 生成指令
    conn.commit()
    #关闭连接
    cursor.close()
    conn.close()
    return "添加成功"

@app.route("/show/user")
def show_user():
    #从数据库获取所有用户信息
    #连接MySQL
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='98765', charset='utf8', db='unicom')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    #发送指令执行sql
    sql = "select * from admin1"
    cursor.execute(sql)  # 生成指令
    user_list = cursor.fetchall()
    #关闭连接
    cursor.close()
    conn.close()
    print(user_list)
    # return ("用户列表")
    #1.找到index.html的文件读取所有内容
    # 2.找到内容中“特殊的占位符”，将数据替换
    # 3.将替换完成的字符串返回给用户的浏览器
    return render_template('show_user.html',user_list = user_list)

@app.route('/action_add_data',methods=["GET","POST"])
def action_add_data():
    if request.method == "GET":
        return render_template("action_add_data.html")
    # print(request.form)
    id = request.form.get("id")
    airline = request.form.get("airline")
    date = request.form.get("date")
    flight_plan_number = request.form.get("flight_plan_number ")
    flight_execution_number= request.form.get("flight_execution_number")
    flight_cancellation_number = request.form.get("flight_cancellation_number")
    cancellation_rate = request.form.get("cancellation_rate")

    #连接MySQL
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='98765', charset='utf8', db='airline_data')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    #发送指令执行sql
    sql = "insert into airline(id,airline,date,flight_plan_number,flight_execution_number,flight_cancellation_number,cancellation_rate) values(%s,%s,%s,%s,%s,%s,%s)"
    # values = (['id'], ['airline'], ['date'], ['flight_plan_number'], ['flight_execution_number'],['flight_cancellation_number'],['cancellation_rate'])
    cursor.execute(sql,[id,airline,date,flight_plan_number,flight_execution_number,flight_cancellation_number,cancellation_rate])  # 生成指令
    conn.commit()
    #关闭连接
    cursor.close()
    conn.close()
    return "添加成功"


@app.route("/index")
def index():
    return render_template("index.html")

@app.route('/add_datalist',methods=["GET","POST"])
def add_datalist():
    if request.method == "GET":
        return render_template("add_datalist.html")
    # print(request.form)
    address = request.form.get("address")
    kind = request.form.get("kind")
    unit = request.form.get("unit")
    sharing = request.form.get("sharing")
    #连接MySQL
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='98765', charset='utf8', db='upload')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    #发送指令执行sql
    sql = "insert into datalist(address,kind,unit,sharing) values(%s,%s,%s,%s)"
    cursor.execute(sql,[address,kind,unit,sharing])  # 生成指令
    conn.commit()
    #关闭连接
    cursor.close()
    conn.close()
    return "添加成功"


@app.route("/datalist")
def datalist():
    #从数据库获取所有用户信息
    #连接MySQL
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='98765', charset='utf8', db='upload')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    #发送指令执行sql
    sql = "select * from datalist"
    cursor.execute(sql)  # 生成指令
    data_list = cursor.fetchall()
    #关闭连接
    cursor.close()
    conn.close()
    print(data_list)
    # return ("用户列表")
    #1.找到index.html的文件读取所有内容
    # 2.找到内容中“特殊的占位符”，将数据替换
    # 3.将替换完成的字符串返回给用户的浏览器
    return render_template('datalist.html',data_list = data_list)

@app.route("/data-visualization")
def data_visualization_():
    return render_template("data-visualization.html")

@app.route("/tables")
def tables():
    return render_template('tables.html')

@app.route("/tables2")
def tables2():
    return render_template('tables2.html')

@app.route("/tables3")
def tables3():
    return render_template('tables3.html')

@app.route("/tables4")
def tables4():
    return render_template('tables4.html')

@app.route("/tables5")
def tables5():
    return render_template('tables5.html')

@app.route("/action_delete_data")
def action_delete_data():
    #从数据库获取所有用户信息
    #连接MySQL
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='98765', charset='utf8', db='airline_data')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    #发送指令执行sql

    sql = "select * from airline where id > %s"
    cursor.execute(sql,41)   # 生成指令
    flight_list = cursor.fetchall()
    #关闭连接
    cursor.close()
    conn.close()
    print(flight_list)
    # return ("用户列表")
    #1.找到index.html的文件读取所有内容
    # 2.找到内容中“特殊的占位符”，将数据替换
    # 3.将替换完成的字符串返回给用户的浏览器
    return render_template('action_delete_data.html',flight_list = flight_list)

@app.route("/action_modify_data")
def action_modify_data():
    return render_template('action_modify_data.html')

@app.route("/preferences")
def preferences_():
    return render_template("preferences.html")

@app.route("/通信")
def connect_():
    return render_template("通信.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            # 获取用户提交的用户名和密码
            username = request.form.get('username')
            password = request.form.get('password')

            # 连接数据库
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='0000',
                database='login',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            cursor = conn.cursor()

            # 检查数据库中是否已经存在该用户名
            cursor.execute("SELECT * FROM register1 WHERE username = %s", (username,))
            result = cursor.fetchone()

            if result:
                # 用户名已存在，返回注册失败的消息
                return jsonify({'status': 'error', 'message': '注册失败，用户名已存在'})
            else:
                # 用户名不存在，插入新用户
                cursor.execute("INSERT INTO register1 (username, password) VALUES (%s, %s)", (username, password))
                conn.commit()
                return jsonify({'status': 'success', 'message': '注册成功'})

        except Exception as e:
            # 处理数据库操作中的任何异常，并打印错误信息
            print(f"Error: {str(e)}")
            return jsonify({'status': 'error', 'message': f'注册失败，发生错误: {str(e)}'})

        finally:
            # 关闭数据库连接
            cursor.close()
            conn.close()

    # 如果是 GET 请求，则渲染注册页面
    return render_template('register.html')

@app.route("/login", methods=["POST"])
def login():
    # 获取用户提交的用户名和密码
    # data = request.get_json()
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        # 检查数据库中是否已经存在该用户名
        # 如果不存在，则将用户名和密码保存到数据库中
        # 如果存在，则返回注册失败的消息
        conn = pymysql.connect(host='localhost', user='root', password='0000', database='login', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM register1 WHERE username = %s", (username,))
        result = cursor.fetchone()
        if result:
            if result['password'] == password:
                return jsonify({'status': 'success', 'message': '登录成功'})
            else:
                return jsonify({'status': 'error', 'message': '密码不匹配'})
        else:
            return jsonify({'status': 'error', 'message': '用户不存在，请注册'})

        cursor.close()
        conn.close()
    return jsonify({'status': 'error', 'message': 'Invalid method'})

@app.route("/fl")
def fl():
    return render_template('fl.html')

@app.route("/cxt", methods=['POST'])
def cxt():
    return render_template('cxt.html')

@app.route("/HFL")
def HFL():

    return render_template('HFL.html')

@app.route("/VFL")
def VFL():
    return render_template('VFL.html')

# 在后端代码中标记满足条件的点，并返回图片和位置信息
def find_first_point(data, threshold):
    for i, point in enumerate(data):
        if point['FedAVG'] >= threshold:
            return i
    return -1

@app.route('/get_data', methods=['GET'])
def get_data():
    selected_dataset = request.args.get('dataset')
    # 从数据库中获取数据
    conn = pymysql.connect(host='localhost', user='root', password='0000', database='plot', charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {selected_dataset}")
    data = cursor.fetchall()
    conn.close()

    # 从结果中提取每一列的数据
    column_names = ['FedAVG', 'FedSAE', 'FedProx', 'NIPAFed']

    result = [[entry['FedAVG'] for entry in data],
              [entry['FedSAE'] for entry in data],
              [entry['FedProx'] for entry in data],
              [entry['NIPAFed'] for entry in data]]

    # 动态生成箱线图
    fig1, ax1 = plt.subplots()
    boxplot = ax1.boxplot([[d[col] for d in data] for col in column_names], patch_artist=True, showfliers=False)
    ax1.set_xticklabels(column_names)
    for patch in boxplot['boxes']:
        patch.set_facecolor('lightblue')  # 设置填充颜色
    ax1.set_xticklabels(column_names)
    plt.ylabel('ACC')

    boxplot_img = io.BytesIO()
    plt.savefig(boxplot_img, format='png')
    boxplot_img.seek(0)
    boxplot_img_encoded = base64.b64encode(boxplot_img.getvalue()).decode()

    # 返回数据集信息和动态生成的图表图片
    return jsonify({'boxplot': boxplot_img_encoded, 'data_deal': result})


@app.route('/get_data1', methods=['GET'])
def get_data1():
    # selected_dataset = request.form.get('dataset')
    selected_dataset = request.args.get('dataset')
    # 从数据库中获取数据
    conn = pymysql.connect(host='localhost', user='root', password='0000', database='plot2', charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {selected_dataset}")
    data = cursor.fetchall()
    conn.close()

    # 从结果中提取每一列的数据
    column_names = ['auc_DP_1', 'auc_DP_2', 'auc_DP_5', 'auc_NDP_1', 'auc_NDP_2', 'auc_NDP_5']

    result = [[entry['auc_DP_1'] for entry in data],
              [entry['auc_DP_2'] for entry in data],
              [entry['auc_DP_5'] for entry in data],
              [entry['auc_NDP_1'] for entry in data],
              [entry['auc_NDP_2'] for entry in data],
              [entry['auc_NDP_5'] for entry in data]]


    # 动态生成箱线图
    fig1, ax1 = plt.subplots()
    boxplot = ax1.boxplot([[d[col] for d in data] for col in column_names], patch_artist=True, showfliers=False)
    ax1.set_xticklabels(column_names)
    for patch in boxplot['boxes']:
        patch.set_facecolor('lightblue')  # 设置填充颜色
    ax1.set_xticklabels(column_names)
    plt.ylabel('ACC')

    boxplot_img = io.BytesIO()
    plt.savefig(boxplot_img, format='png')
    boxplot_img.seek(0)
    boxplot_img_encoded = base64.b64encode(boxplot_img.getvalue()).decode()
    # plt.show()

    # 返回数据集信息和动态生成的图表图片
    return jsonify({'boxplot': boxplot_img_encoded, 'data_deal': result})

if __name__ == '__main__':
    app.run(debug=True)
