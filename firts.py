# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 11:11:44 2021

@author: jarias
"""

print('Inicia el programa')

import sqlite3

conn = sqlite3.connect('TestDB.db')  # You can create a new database by changing the name within the quotes
c = conn.cursor() # The database will be saved in the location where your 'py' file is saved

# Create tables

c.execute('''CREATE TABLE weater ([id] INTEGER PRIMARY KEY AUTOINCREMENT,[read_date] DateTime,[temperature] numeric(12,6),[humidity] numeric(12,6))''')

c.execute('''CREATE TABLE exchange ([id] INTEGER PRIMARY KEY AUTOINCREMENT,[read_date] DateTime,[origin_currency] text, [origin_value] numeric(12,6) ,[change_currency] text, [change_value] numeric(12,6) )''')

c.execute('''INSERT INTO exchange(read_date, origin_currency,origin_value,change_currency,change_value) values('2021/09/10', 'Euro','1.00','Dolar','1.145' ) ''')
c.execute('''INSERT INTO exchange(read_date, origin_currency,origin_value,change_currency,change_value) values('2021/09/11', 'Euro','1.00','Dolar','1.150' ) ''')
c.execute('''INSERT INTO exchange(read_date, origin_currency,origin_value,change_currency,change_value) values('2021/09/12', 'Euro','1.00','Dolar','1.151' ) ''')
c.execute('''INSERT INTO exchange(read_date, origin_currency,origin_value,change_currency,change_value) values('2021/09/13', 'Euro','1.00','Dolar','1.116' ) ''')
c.execute('''INSERT INTO exchange(read_date, origin_currency,origin_value,change_currency,change_value) values('2021/09/14', 'Euro','1.00','Dolar','1.160' ) ''')

c.close()
