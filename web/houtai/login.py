from flask import Flask, request, jsonify, send_from_directory,abort
from datetime import datetime, date
import sqlite3 as lite
import sys
import json


app = Flask(__name__)

con = lite.connect('picture_share.db', check_same_thread=False)

with con:
    cur = con.cursor()
    cur.execute('SELECT SQLITE_VERSION()')
    data = cur.fetchone()
    print "SQLite version: %s" % data



@app.route('/')
def send_js():
    return send_from_directory('..','index.html')

@app.route('/style.css')
def send_jsa():
    return send_from_directory('..','style.css')


@app.route('/app.js')
def send_jsaa():
    return send_from_directory('..','app.js')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return do_the_register()
    else:
        return show_the_register_form()

def show_the_register_form():
    #need to render login form
    return 'OK'

def do_the_register():
    request.form = request.get_json()
    print 'username:' + request.form['username']
    print 'password:' +request.form['password']
    with con:
        cur = con.cursor()
        sql_command = """insert into users values('""" + request.form['username'] + """', '""" + request.form['password'] + """')"""
        print sql_command
        cur.execute(sql_command)
    return 'OK'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()

def show_the_login_form():
    #need to render login form
    return 'OK'

def do_the_login():
    request.form = request.get_json()
    print 'username:' + request.form['username']
    print 'password:' +request.form['password']
    with con:
        cur = con.cursor()
        sql_command = """select * from users where email='""" + request.form['username'] + """' AND password='""" + request.form['password'] + """'"""
        print sql_command
        cur.execute(sql_command)
        data = cur.fetchone()
        json_data = json.dumps(data)
        print json_data
        if json_data == 'null':
            abort(401)
        else:
            return json_data
    return 'OK'


@app.route('/circle_amount/<username>', methods=['GET'])
def circle_amount(username):
    return get_circle_amount(username)

def get_circle_amount(username):
    print 'username:' + username
    with con:
        cur = con.cursor()
        sql_command = """select MAX(circle) from friends where email1='""" + username + """'"""
        print sql_command
        jsondata = []
        for row in cur.execute(sql_command):
            jsondata.append({'circles',row[0]})
        return jsonify(jsondata)
    return 'OK'

@app.route('/delete_friend/<username>', methods=['POST'])
def delete_friend(username):
    return do_delete_friend(username)

def do_delete_friend(username):
    request.form = request.get_json()
    print 'username:' + username
    print 'friendname:' + request.form['friend_name']
    with con:
        cur = con.cursor()
        sql_command = """DELETE FROM friends WHERE (email1='""" + username + """' AND email2='""" + request.form['friend_name'] + """') OR (email1='""" + request.form['friend_name']  + """'AND email2= '""" + username + """')"""
        cur.execute(sql_command)
    print sql_command
    return 'OK'

@app.route('/add_circle/<username>',methods=['POST'])
def add_circle(username):
    return do_add_circle(username)

def do_add_circle(username):
    request.form = request.get_json()
    print 'username:' + username
    print 'friendname:' + request.form['friend_name']
    print 'circle_num:' + str(request.form['circle_num'])
    with con:
        cur = con.cursor()
        sql_command = """UPDATE friends SET circle='""" + str(request.form['circle_num']) + """' WHERE (email1='""" + username + """' AND email2='""" + request.form['friend_name'] + """')"""
        cur.execute(sql_command)
    return 'OK'


@app.route('/change_pass/<username>',methods=['POST'])
def change_pass(username):
    return do_change_pass(username)

def do_change_pass(username):
    #request.form = request.get_json()
    print 'username:' + username
    print 'pass:' + str(request.form['pass'])
    with con:
        cur = con.cursor()
        sql_command = """UPDATE users SET password='""" + str(request.form['pass']) + """' WHERE (email='""" + username + """')"""
        cur.execute(sql_command)
    return 'OK'




@app.route('/waitlist/<username>', methods=['GET'])
def waitlist(username):
    if request.method == 'POST':
        return do_the_add()
    else:
        return show_the_add_form(username)


@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        return do_the_add()


def show_the_add_form(username):
    print 'username:' + username
    with con:
        cur = con.cursor()
        sql_command = """select email2 from waitlist where email1='""" + username + """'"""
        print sql_command
        data = []
        jsondata = []
        for row in cur.execute(sql_command):
            data.append(row[0])
        jsondata.append(['waiting list',data])
        if jsondata == []:
            return 'NO people'
        else:
            return jsonify(jsondata)
    return 'OK'

def do_the_add():
    request.form = request.get_json()
    print 'username:' + request.form['username']
    print 'target:' + request.form['target']

    with con:
        cur = con.cursor()
        sql_command = """insert into waitlist values('""" + request.form['target'] + """', '""" + request.form['username'] + """')"""
        print sql_command
        cur.execute(sql_command)
    return 'OK'


@app.route('/response', methods=['POST'])
def response():
    if request.method == 'POST':
        return do_the_response()


def do_the_response():
    request.form = request.get_json()
    print 'username:' + request.form['username']
    print 'target:' + request.form['target']
    print 'result:' + request.form['result']
    with con:
        cur = con.cursor()
        if request.form['result'] == 'accept':
                    sql_command = """insert into friends values('""" + request.form['target'] + """', '""" + request.form['username'] + """', 0)"""
                    print sql_command
                    cur.execute(sql_command)
                    sql_command = """insert into friends values('""" + request.form['username'] + """', '""" + request.form['target'] + """', 0)"""
                    print sql_command
                    cur.execute(sql_command)
        sql_command = """DELETE FROM waitlist where email1='""" + request.form['username'] + """' and email2='"""+request.form['target'] + """'"""
        print sql_command
        cur.execute(sql_command)
    return 'OK'


@app.route('/search/<username>', methods=['GET'])
def search(username):
    return show_the_search_form(username)




def show_the_search_form(username):
    print 'username:' + username
    with con:
        cur = con.cursor()
        data=[]
        sql_command = """select email from users where email='""" + username + """'"""
        print sql_command
        cur.execute(sql_command)
        row_data = cur.fetchone()
        json_data = json.dumps(data)
        print json_data
        if json_data == 'null':
            return 'NO Such User'
        else:
            return json_data
    return 'OK'




@app.route('/friends/<username>', methods=['GET'])
def friends(username):
    return show_the_friends_form(username)

def show_the_friends_form(username):
    print 'username:' + username
    with con:
        cur = con.cursor()
        sql_command = """select email2,circle from friends where email1='""" + username + """'"""
        print sql_command
        jsondata = []
        for row in cur.execute(sql_command):
            data = {}
            data['email'] = row[0];
            data['circle'] = row[1];
            jsondata.append(data)
        return jsonify({"friends":jsondata})
    return 'OK'

@app.route('/post',methods=['POST'])

def post():
    if request.method == 'POST':
        return do_the_post()

def do_the_post():
    request.form = request.get_json()
    print 'username:' + request.form['username']
    print 'text:' + request.form['text']
    print 'circle:' + str(request.form['circle'])
    print 'picture:' + request.form['picture']
    t = datetime.now()
    print t
    t = t.strftime('%Y-%m-%d %H:%M:%S')
    print t
    with con:
        cur = con.cursor()
        sql_command = """insert into posts values('""" + request.form['username'] + """', '""" + request.form['text'] + """', '""" + str(request.form['circle']) + """','""" + request.form['picture'] + """','""" + t + """')"""
        print sql_command
        cur.execute(sql_command)
    return 'OK'


@app.route('/newsfeed',methods=['POST'])

def news_feed():
    if request.method == 'POST':
        return do_news_feed()

def do_news_feed():
    request.form = request.get_json()
    print 'username:' + request.form['username']
    with con:
        cur = con.cursor()
        sql_command = """SELECT DISTINCT p.text, p.owner,p.time,p.picture_uri from posts p, friends f WHERE p.owner = '""" + request.form['username'] + """' OR (f.email2 = '""" + request.form['username'] + """' and f.email1 = p.owner and f.circle = p.circle) ORDER BY p.time DESC"""
        print sql_command
        jsondata = []
        for row in cur.execute(sql_command):
            data = {}
            data['text'] = row[0]
            data['owner'] = row[1]
            data['picture'] = row[3]
            #jsondata[i].append(['text',row[0]])
            #jsondata[i].append(['owner',row[1]])
            #jsondata[i].append(['time',row[2]])
            jsondata.append(data)
           # data.append(row)
        return jsonify({"feed":jsondata})
    return 'OK'




if __name__ == '__main__':
    app.debug = True
    app.run()
