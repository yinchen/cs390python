from flask import Flask, request, jsonify
from flask.ext.cors import CORS
import sqlite3 as lite
import sys
import json


app = Flask(__name__)
cors = CORS(app)


con = lite.connect('picture_share.db', check_same_thread=False)

with con:
    cur = con.cursor()    
    cur.execute('SELECT SQLITE_VERSION()')
    data = cur.fetchone()
    print "SQLite version: %s" % data

    
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
        data = []
        jsondata = []
        for row in cur.execute(sql_command):
            data.append(row)
        jsondata.append(['friends',data])
        if jsondata == []:
            return 'NO people'
        else:
            return jsonify(jsondata)
    return 'OK'









if __name__ == '__main__':
    app.debug = True
    app.run()
