import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
import json

DATABASE = 'scantron.db'

######################################################################################################################################


def init_db():
    #create database and tables
    
    sqliteDB = sqlite3.connect(DATABASE)
    print ("Opened database successfully")

    #sqliteDB.execute('DROP TABLE IF exists test')
    sqliteDB.execute('CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY AUTOINCREMENT, subject TEXT, answer_keys TEXT)')

    #sqliteDB.execute('DROP TABLE IF exists scantron')
    sqliteDB.execute('CREATE TABLE IF NOT EXISTS scantron (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, test_id INTEGER, score INTEGER, result TEXT, url TEXT, format TEXT, scantron TEXT)')

    print ("Tables created successfully")


def create_test(subject, answer_keys):
    sqliteDB = sqlite3.connect(DATABASE)
    cur = sqliteDB.cursor()
    cur.execute("INSERT INTO test (subject,answer_keys) VALUES (?,?)",(subject, answer_keys))
    sqliteDB.commit()
    cur.execute("SELECT MAX(id) FROM test")
    result = cur.fetchone()
    cur_id = result[0]
    cur.close()
    sqliteDB.close()
    return cur_id

def create_scantron(name, test_id, format, url, score, result, scantron):
    sqliteDB = sqlite3.connect(DATABASE)
    cur = sqliteDB.cursor()
    cur.execute("INSERT INTO scantron (name, test_id, score, result, url, format, scantron) VALUES (?,?,?,?,?,?,?)",(name, test_id, score, result, url, format, scantron))
    sqliteDB.commit()
    cur.execute("SELECT MAX(id) FROM scantron")
    result = cur.fetchone()
    cur_id = result[0]
    cur.close()
    sqliteDB.close()
    return cur_id

def get_test(id):
    sqliteDB = sqlite3.connect(DATABASE)
    cur = sqliteDB.cursor()
    cur.execute("SELECT subject, answer_keys FROM test WHERE id=(?)", (id,))
    result = cur.fetchone()
    subject = result[0]
    answer_keys = result[1]
    cur.close()
    sqliteDB.close()
    return subject, answer_keys

def get_scantrons(test_id):
    scantrons = []
    sqliteDB = sqlite3.connect(DATABASE)
    cur = sqliteDB.cursor()
    cur.execute("SELECT id, name, score, result, url FROM scantron WHERE test_id=(?)", (test_id,))
    res = cur.fetchall()
    for s in res:
        cur_scantron = dict()
        cur_scantron['scantron_id'] = s[0]
        cur_scantron['name'] = s[1]
        subject,_ = get_test(test_id)
        cur_scantron['subject'] = subject
        cur_scantron['score'] = s[2]
        cur_scantron['result'] = s[3]
        cur_scantron['scantron_url'] = s[4]
        scantrons.append(cur_scantron)
    cur.close()
    sqliteDB.close()
    return scantrons

def get_scantron(file_name):
    sqliteDB = sqlite3.connect(DATABASE)
    cur = sqliteDB.cursor()
    cur.execute("SELECT scantron FROM scantron ")
    res = cur.fetchone()[0]
    
    cur.close()
    sqliteDB.close()
    return res

init_db()