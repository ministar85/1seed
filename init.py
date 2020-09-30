from flask import Flask, render_template, flash, redirect, url_for, session, logging, request, Markup,jsonify
from wtforms import Form, StringField, IntegerField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from wtforms import DateField
from array import *
from flask import Blueprint
import simplejson as json
from flask import Blueprint, render_template
########
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#adds date picker for all date type
from wtforms.fields.html5 import DateField


#####################
app = Flask(__name__)
app.debug=True

#Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
           return f(*args, **kwargs)
        else:
           flash('Unauthorized, Please login', 'danger')
           return redirect(url_for('login'))
    return wrap

#####################
#####################
#config mysql
from flask_mysqldb import MySQL
#app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_HOST'] = '192.168.0.25'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pw0rd4gr33nhouse!'
app.config['MYSQL_DB'] = 'greenhouse'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#initialize Mysql
mysql = MySQL(app)
#####################
#####################
