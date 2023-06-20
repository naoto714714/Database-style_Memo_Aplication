# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, redirect, url_for
import csv
import mysql.connector as sqlconn
import re
import urllib
import json

app = Flask(__name__)

conn = sqlconn.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    password = ''
    )

#接続が切れたときに再接続してくれるように設定
conn.ping(reconnect = True)

#接続できているか確認
print(conn.is_connected())

#カーソルの生成
cur = conn.cursor() 

@app.route('/', methods=['GET', 'POST'])
def login():
    # ２回目以降データが送られてきた時の処理です
    if request.method == 'POST':
        id = request.form['id']
        userList = []
        userList.append(id)
        userList.append(0)
        with open('templates/login.csv', 'a', newline="", encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(userList)
                f.close()
        
        for num in range(1,5):
            #作成するデータベース名を入力
            db_name = id + str(num)

            #もし同じ名前のデータベースが存在していたら削除
            sql = 'DROP DATABASE IF EXISTS ' + db_name
            cur.execute(sql)

            #データベースの作成
            sql = 'CREATE DATABASE ' + db_name
            cur.execute(sql)
        
        #データベースに加えた変更を反映させる
        conn.commit()
        
        return render_template('index.html')
    # １回目のデータが何も送られてこなかった時の処理です。
    else:
        return render_template('login_form.html')

@app.route('/loginCheck')
def loginCheck():
    return render_template('login.csv')

@app.route('/signup')
def signup():
    return render_template('sign_up.html')

@app.route('/home/<user_id>', methods=['GET', 'POST'])
def home(user_id):
    if request.method == 'POST':
        return render_template('index.html', user_id = user_id, text ="テキスト")
    else:
        db_name = user_id + str(1)
        sql = 'USE ' + db_name
        cur.execute(sql)
        conn.commit()
        return render_template('index.html', user_id = user_id, text = "テキスト")
    
@app.route('/dbChange', methods=['GET', 'POST'])
def dbChange():
    if request.method == 'POST':
        user_id = request.form['user_id']
        dbType = request.form['dbType']
        print(user_id)
        print(dbType)
        db_name = ""
        
        if (dbType == "db1"):
            db_name = user_id + str(1)
        elif(dbType == "db2"):
            db_name = user_id + str(2)
        elif(dbType == "db3"):
            db_name = user_id + str(3)
        elif(dbType == "db4"):
            db_name = user_id + str(4)
        
        sql = 'USE ' + db_name
        cur.execute(sql)
        conn.commit()
        
        return "None"
    
@app.route('/controlChange', methods=['GET', 'POST'])
def controlChange():
    if request.method == 'POST':
        user_id = request.form['user_id']
        contType = request.form['type']
        print(user_id)
        print(contType)
        if (contType == "作成"):
            print("作成します")
        elif(contType == "追加"):
            print("追加します")
        elif(contType == "変更"):
            print("変更します")
        elif(contType == "削除"):
            print("削除します")
        return "None"

@app.route('/create',  methods=['GET', 'POST'])
def Create():
    if request.method == 'POST':
        user_id = request.form['user_id']
        columnNum = request.form['columnNum']
        tableName = request.form['tableName']
        print(user_id)
        print(columnNum)
        print(tableName)
        print()
        if (tableName == "郵便番号"):
            sql = 'create table 郵便番号 (郵便番号 INT, 都道府県 CHAR(255), 市区町村 CHAR(255), 町域 CHAR(255))';
            cur.execute(sql)
            conn.commit()
            print("郵便番号")
            return "None"
        
        if (tableName == "天気予報"):
            sql = 'create table 天気予報 (日付 CHAR(255), 地域 CHAR(255), 天気 CHAR(255), 最高気温 FLOAT)';
            cur.execute(sql)
            conn.commit()
            print("天気予報")
            return "None"
        
        if (columnNum == "1"):
            colName1 = request.form['colName1']
            colType1 = request.form['colType1']
            sql = 'create table if not exists ' + tableName + '(' + colName1 + colType1 + ')';
            cur.execute(sql)
            conn.commit()
            print("1です")
        elif(columnNum == "2"):
            colName1 = request.form['colName1']
            colType1 = request.form['colType1']
            colName2 = request.form['colName2']
            colType2 = request.form['colType2']
            sql = 'create table if not exists ' + tableName + '(' + colName1 + colType1 + ',' + colName2 + colType2 + ')';
            cur.execute(sql)
            conn.commit()
            print("２です")
        elif(columnNum == "3"):
            colName1 = request.form['colName1']
            colType1 = request.form['colType1']
            colName2 = request.form['colName2']
            colType2 = request.form['colType2']
            colName3 = request.form['colName3']
            colType3 = request.form['colType3']
            sql = 'create table if not exists ' + tableName + '(' + colName1 + colType1 + ',' + colName2 + colType2 + ',' + colName3 + colType3 + ')';
            cur.execute(sql)
            conn.commit()
            print("３です")
        elif(columnNum == "4"):
            colName1 = request.form['colName1']
            colType1 = request.form['colType1']
            colName2 = request.form['colName2']
            colType2 = request.form['colType2']
            colName3 = request.form['colName3']
            colType3 = request.form['colType3']
            colName4 = request.form['colName4']
            colType4 = request.form['colType4']
            sql = 'create table if not exists ' + tableName + '(' + colName1 + colType1 + ',' + colName2 + colType2 + ',' + colName3 + colType3 + ',' + colName4 + colType4 + ')';
            cur.execute(sql)
            conn.commit()
            print("４です")
        return "None"

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        user_id = request.form['user_id']
        tableName = request.form['tableName']
        data = request.form['data']
        #print("ユーザー名:" + user_id)
        #print("テーブル名：" + tableName)
        #print("データ：" + data)
        print()
        
        if (tableName == "郵便番号"):
            base_url = "https://zipcloud.ibsnet.co.jp/api/search"
            response = urllib.request.urlopen(base_url + "?zipcode=" + data)
            content = json.loads(response.read().decode('utf8'))
            dt1 = data
            dt2 = "'" + (content["results"][0]["address1"]) + "'"
            dt3 = "'" + (content["results"][0]["address2"]) + "'"
            dt4 = "'" + (content["results"][0]["address3"]) + "'"
            sql = "insert into " + tableName + " values (" + dt1 + "," + dt2 + "," + dt3 + "," + dt4 + ")"
            cur.execute(sql)
            conn.commit()
            return "None"
        
        if (tableName == "天気予報"):
            base_url = "https://www.jma.go.jp/bosai/forecast/data/forecast/"
            response = urllib.request.urlopen(base_url + data + ".json")
            content = json.loads(response.read().decode('utf8'))

            dt1 = "'" + (content[1]['timeSeries'][0]['timeDefines'][0]) + "'"
            dt2 = "'" + (content[1]['tempAverage']['areas'][0]['area']['name']) + "'"
            dt3 = "'" + (content[0]['timeSeries'][0]['areas'][0]['weathers'][1]) + "'"
            dt4 = "'" + (content[1]['tempAverage']['areas'][0]['max']) + "'"

            sql = "insert into " + tableName + " values (" + dt1 + "," + dt2 + "," + dt3 + "," + dt4 + ")"
            cur.execute(sql)
            conn.commit()
            return "None"
        
        sql = "select count(*) from information_schema.columns where table_name = '" + tableName + "'"
        cur.execute(sql)

        #すべてのデータをリスト形式で取得
        colNum = cur.fetchone()
        if (colNum[0] == 1):
            print("カラム数：１")
            p = re.compile("(.*)")
            m = p.search(data)
            dt1 = "'" + m.group(1) + "'"
            if (dt1 == "''"):
                dt1 = "default"
            sql = "insert into " + tableName + " values (" + dt1 + ")"
            cur.execute(sql)
            conn.commit()
        elif (colNum[0] == 2):
            print("カラム数：２")
            p = re.compile("(.*)\,(.*)")
            m = p.search(data)
            dt1 = "'" + m.group(1) + "'"
            dt2 = "'" + m.group(2) + "'"
            if (dt1 == "''"):
                dt1 = "default"
            if (dt2 == "''"):
                dt2 = "default"
            sql = "insert into " + tableName + " values (" + dt1 + "," + dt2 + ")"
            cur.execute(sql)
            conn.commit()
        elif (colNum[0] == 3):
            print("カラム数：３")
            p = re.compile("(.*)\,(.*)\,(.*)")
            m = p.search(data)
            dt1 = "'" + m.group(1) + "'"
            dt2 = "'" + m.group(2) + "'"
            dt3 = "'" + m.group(3) + "'"
            if (dt1 == "''"):
                dt1 = "default"
            if (dt2 == "''"):
                dt2 = "default"
            if (dt3 == "''"):
                dt3 = "default"
            sql = "insert into " + tableName + " values (" + dt1 + "," + dt2 + "," + dt3 + ")"
            cur.execute(sql)
            conn.commit()
        elif (colNum[0] == 4):
            print("カラム数：４")
            p = re.compile("(.*)\,(.*)\,(.*)\,(.*)")
            m = p.search(data)
            dt1 = "'" + m.group(1) + "'"
            dt2 = "'" + m.group(2) + "'"
            dt3 = "'" + m.group(3) + "'"
            dt4 = "'" + m.group(4) + "'"
            if (dt1 == "''"):
                dt1 = "default"
            if (dt2 == "''"):
                dt2 = "default"
            if (dt3 == "''"):
                dt3 = "default"
            if (dt4 == "''"):
                dt4 = "default"
            sql = "insert into " + tableName + " values (" + dt1 + "," + dt2 + "," + dt3 + "," + dt4 + ")"
            cur.execute(sql)
            conn.commit()
        else:
            print("テーブル名が存在しません")
            
        return "None"

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        user_id = request.form['user_id']
        tableName = request.form['tableName']
        columnName = request.form['columnName']
        before = request.form['before']
        after = request.form['after']
        print("ユーザー名：" + user_id)
        print("テーブル名：" + tableName)
        print("カラム名：" + columnName)
        print("変更前：" + before)
        print("変更後：" + after)
        print()
        sql = 'update ' + tableName + ' set ' + columnName + '="' + after + '" where ' + columnName + '="' + before + '"'
        cur.execute(sql)
        conn.commit()
        
        return "None"
    
@app.route('/delete', methods=['GET', 'POST'])
def Delete():
    if request.method == 'POST':
        user_id = request.form['user_id']
        tableName = request.form['tableName']
        columnName = request.form['columnName']
        data = request.form['data']
        print("ユーザー名：" + user_id)
        print("テーブル名：" + tableName)
        print("カラム名：" + columnName)
        print("削除するデータ：" + data)
        print()
        sql = 'delete from ' + tableName + ' where ' + columnName + '="' + data +'"'
        cur.execute(sql)
        conn.commit()
        
        return "None"
    
@app.route('/search', methods=['GET', 'POST'])
def Search():
    if request.method == 'POST':
        user_id = request.form['user_id']
        tableName = request.form['tableName']
        columnName = request.form['columnName']
        sign = request.form['sign']
        data = request.form['data']
        print("ユーザー名：" + user_id)
        print("テーブル名：" + tableName)
        print("カラム名：" + columnName)
        print("等号：" + sign)
        print("検索するデータ：" + data)
        print()
        
        sql = 'select * from ' + tableName + ' where ' + columnName + sign + '"' + data +'"'
        cur.execute(sql)
        res = cur.fetchall()
        
        sql = 'show columns from ' + tableName
        cur.execute(sql)
        resCol = cur.fetchall()
        colList = []
        for row in resCol:
            colList.append(row[0])
        
        with open('templates/search.csv', 'w', newline="", encoding='utf_8_sig') as f:
                writer = csv.writer(f)
                writer.writerow(colList)
                for row in res:
                    writer.writerow(row)
                f.close()
                
        return "none"
    
@app.route('/searchAll', methods=['GET', 'POST'])
def SearchAll():
    if request.method == 'POST':
        user_id = request.form['user_id']
        tableName = request.form['tableName']
        print("ユーザー名：" + user_id)
        print("テーブル名：" + tableName)
        print()
        
        sql = 'select * from ' + tableName
        cur.execute(sql)
        res = cur.fetchall()
        
        sql = 'show columns from ' + tableName
        cur.execute(sql)
        resCol = cur.fetchall()
        colList = []
        for row in resCol:
            colList.append(row[0])
        
        with open('templates/searchAll.csv', 'w', newline="", encoding='utf_8_sig') as f:
                writer = csv.writer(f)
                writer.writerow(colList)
                for row in res:
                    writer.writerow(row)
                f.close()
                
        return "none"

@app.route('/search_csv')
def Search_csv():
    return render_template('search.csv')

@app.route('/searchAll_csv')
def searchAll_csv():
    return render_template('searchAll.csv')

@app.route('/close')
def close():
        #カーソルをクローズ
        cur.close()

        #コネクションをクローズ
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)