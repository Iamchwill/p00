# BlueGreen (Edwin Zheng, Shriya Anand, Zhaoyu Lin)
# SoftDev
# K16: All About Database
# Oct 22, 2021
from flask import Flask, render_template, request, session     #facilitate flask webservingimport
import os

app = Flask(__name__)    #create Flask object
app.secret_key = os.urandom(32) #create random key

import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O


DB_FILE="discobandit.db" #this is the original file

               #facilitate db ops -- you will use cursor to trigger db events

#==========================================================
# if(c.execute("EXISTS")):
#     c.execute("CREATE TABLE userinfo (username TEXT, password TEXT)")
#     print("create table works") #this creates a new table
@app.route('/login.html',methods = ['GET','POST'])
def addrec():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            with sql.connect(DB_FILE) as db:
                    #open if file exists, otherwise create
                    c = db.cursor()
                    c.execute("INSERT INTO userinfo (username,password) VALUES (?,?)",(username,password) )

                    db.commit()
                    msg = "Record successfully added"
                    db.close()
        except:
            print("error")
def list():
   con = sql.connect(DB_FILE)
   con.row_factory = sql.Row

   cur = con.cursor()
   cur.execute("select * from userinfo")

   rows = cur.fetchall();
   return render_template("list.html",rows = rows)

if __name__ == '__main__':
   app.run(debug = True)
#==========================================================

# db.commit() #save changes
# db.close()  #close database
