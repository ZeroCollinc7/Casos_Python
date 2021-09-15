# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 11:54:30 2021

@author: Joffre Arias.
"""
from time import time, sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import sqlite3
import urllib.request

#Carga el driver de Crome para ejecutar la carga del sitio o página
driver = webdriver.Chrome(ChromeDriverManager().install())

#Función que inserta los datos leidos desde el sitio
def insert_data(temperature,humidity):
    '''Función que almacena en Base de datos las lecturas realizadas'''
    try:
        sqliteConnection = sqlite3.connect('TestDB.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")        
     
        insert_var = "INSERT INTO weater(read_date,temperature,humidity) values(DATETIME('now'),%d,%d)"%(temperature,humidity)
                
        sqlite_insert_query = insert_var

        count = cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()
        print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if sqliteConnection:
                sqliteConnection.close()
                print("The SQLite connection is closed")
                
                return True

#Función que obtiene los datos lamacenados en DB / Conecta a la base de datos 
def db(database_name='TestDB.db'):
    return sqlite3.connect(database='TestDB.db')

def query_db(query, args=(), one=False):
    cur = db().cursor()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()
    return (r[0] if r else None) if one else r


#Función que lee los datos desde el sitio
def read_data():
    '''Función para leer los datos de temperatura y humedad del sitio'''
    driver.get("https://dweet.io/follow/thecore")
    content = driver.page_source
    soup = BeautifulSoup(content)
    results = soup.find("pre", {"id": "thing-data-raw"}).text
    data = json.loads(results)
    insert_data(data["temperature"],data["humidity"])
    
    return insert_data

def do_work(data):
        #Funcion que envia los resultados al webhook   
        body = json.dumps(data)
        print(body)
        myurl = "https://webhook.site/bf80619c-b624-488f-974e-6cf43972af4b"
        req = urllib.request.Request(myurl)
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        jsondata = json.dumps(body)
        jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
        req.add_header('Content-Length', len(jsondataasbytes))
        response = urllib.request.urlopen(req, jsondataasbytes)
        
        return response

#Variables de inicio de proceso, o cantidad de iteraciones
x = [1,15]

def guru( funct, *args ):
    funct( *args )
    
def inicia_proceso( arg ):
    i = arg[0]
    while True:
        sleep(60 - time() % 60)
        read_data()
        i+=1   
        if (i>=arg[1]):  
            readers = query_db("select * from weater")   
            do_work(readers)
            break  
    return print (arg)

#CALL A REGULAR FUNCTION THRU A LAMBDA
guru(lambda v : inicia_proceso(v),x)