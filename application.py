#!/usr/bin/env python
# coding=utf-8

from flask import Flask, request, redirect, url_for, render_template
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'mydb'
mongo = PyMongo(app)

@app.route('/')
def index():
    users = mongo.db.users.find()
    return render_template('index.html', users=users)

def valid_login(username, password):
    valid = False
    user = mongo.db.users.find({"name":username}, {"_id":0,"name":1,"pass":1})
    if user:
        for u in user:
            if u['name'] == username:
                valid = True
    else:
        print "user null"
    return valid

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == "POST":
        if valid_login(request.form['username'], request.form['password']):
            return redirect(url_for('index'))
        else:
            error = 'invalid username/password'
    return render_template('login.html', error=error)

if __name__ == "__main__":
    app.run()
