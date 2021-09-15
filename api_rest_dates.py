# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 09:07:48 2021

@author: Joffre Arias
"""
#
import json
import sqlite3
from flask import Flask
import urllib.request

#Conecta a la base de datos 
def db(database_name='TestDB.db'):
    return sqlite3.connect(database='TestDB.db')

def query_db(query, args=(), one=False):
    cur = db().cursor()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()
    return (r[0] if r else None) if one else r

def do_work(data):
        # do something that takes a long time      
        body = json.dumps(data)      
        myurl = "https://webhook.site/bf80619c-b624-488f-974e-6cf43972af4b"
        req = urllib.request.Request(myurl)
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        jsondata = json.dumps(body)
        jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
        req.add_header('Content-Length', len(jsondataasbytes))
        response = urllib.request.urlopen(req, jsondataasbytes)
        
        return response

#Obtiene el cambio de monedas almacenados en base de datos
my_query = query_db("select * from exchange")

#Convierte la consulta a formato json
json_output = json.dumps(my_query)

#Api Rest conulta resutlados en formato JSON
api = Flask(__name__)

@api.route('/exchages', methods=['GET'])
def start_task():       
    do_work(json_output)    
    return json.dumps(json_output)

if __name__ == '__main__':
    api.run()
    


