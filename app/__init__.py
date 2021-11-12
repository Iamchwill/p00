# BlueGreen (Edwin Zheng, Shriya Anand, Zhaoyu Lin)
# SoftDev
# K15: Sessions Greetings
# Oct 20, 2021

import re
from flask import Flask, render_template, request, session     #facilitate flask webservingimport
import os
import sqlite3

app = Flask(__name__)    #create Flask object
app.secret_key = os.urandom(32) #create random key
DB_FILE = "discobandit.db"
@app.route("/") #,methods=['GET', 'POST'])
def disp_loginpage():
    response = ""
    if "userID" not in session: #check if there is the correct user name stored in session
        addrec()
        return render_template( 'login.html', login_fail = "" ) #return login page if correct user name is not stored in session
    else:
        with sqlite3.connect(DB_FILE) as db:
            c = db.cursor()
            c.execute("select BlogID from userinfo WHERE username LIKE '%" + str(session['userID']) + "%';")
            blogID = c.fetchone()
            for row in blogID:
                ID = row
            c.row_factory = sqlite3.Row
            ID = str(ID)
            c.execute("select BlogTitle from bloginfo WHERE BlogID LIKE '%" + ID + "%';")
            blog = c.fetchall()
            c.close()
        return render_template('response.html', user = session.get("userID")) #return response page if correct user name is stored in session

@app.route("/auth", methods=['GET', 'POST'])
def authenticate():
    response = "TRY AGAIN: "
    if request.args['password'] == "" or request.args['password'] == " " or request.args['password'] == None:
            response += " Username or password cannot be blank"
    if(check_existence('username', request.args['username']) == False or check_existence('password', request.args['password']) == False): #checks for password
        response += "incorrect username or password"
    #checks if user exists and password matches user
    if(response == "TRY AGAIN: "):
        session['userID'] = request.args['username']
        with sqlite3.connect(DB_FILE) as db:
            c = db.cursor()
            c.execute("select BlogID from userinfo WHERE username LIKE '%" + str(session['userID']) + "%';")
            blogID = c.fetchone()
            for row in blogID:
                ID = row
            c.row_factory = sqlite3.Row
            ID = str(ID)
            c.execute("select BlogTitle from bloginfo WHERE BlogID LIKE '%" + ID + "%';")
            blog = c.fetchall()
            c.close()
        return render_template('response.html', user = request.args['username'], blog = blog)
    else:
        return render_template('login.html', login_fail = response) #Else, return the response telling you what's wrong


@app.route("/reg1", methods=['GET', 'POST'])
def reg1():
    return render_template('register.html')

@app.route("/reg2", methods=['GET', 'POST'])
def reg2():
    error = "ERROR: "
    error += validate("userID", request.args['regUser'])
    error += validate("password", request.args['regPass'])
    if (error == "ERROR: "):
        #if userID is valid, store in database
        session["userID"] = request.args['regUser']
        insert("userinfo", request.args['regUser'], request.args['regPass'])

        return render_template('response.html',user = request.args['regUser'])
            # ADD USERID TO THE DB HERE

    return render_template('register.html', error = error)
    # return render_template('response.html', user = session.get("userID"))

@app.route("/createblog", methods=['GET', 'POST'])
def createblog():
    error = "ERROR: "
    blogtitle = request.args['blogtitle']
    username = session['userID']
    print(username)
    
    with sqlite3.connect(DB_FILE) as db:
        c = db.cursor()
        c.execute("select BlogID from userinfo WHERE username LIKE '%" + str(username) + "%';")
        blogID = c.fetchone()
        for row in blogID:
            ID = row
        print(ID)
        

        c = db.cursor()
        c.row_factory = sqlite3.Row
        ID = str(ID)
        c.execute("select BlogTitle from bloginfo WHERE BlogID LIKE '%" + ID + "%';")
        blog = c.fetchall()
        error += validate("blogtitle", request.args['blogtitle'])
        if(error == "ERROR: "):
            c.execute("INSERT INTO bloginfo (BlogTitle, BlogID) VALUES (?,?)",(str(blogtitle), ID) )
            print("blog added")
            c.execute("select BlogTitle from bloginfo WHERE BlogID LIKE '%" + ID + "%';")
            blog = c.fetchall()
            return render_template('response.html', user = username, blog = blog)
        else:
            print("*****" + error)
            return render_template('response.html', user = username, blog = blog, login_fail = error)
    

@app.route("/createentries", methods=['GET', 'POST'])
def createentries():
    if request.method == 'POST':
        blogtitle = request.form['createentry']
        with sqlite3.connect(DB_FILE) as db:
            entrynum = 0
            entrytitle = request.args['entrytitle']
            entry = request.args['entry']
            c = db.cursor()
            c.execute("select EntryNum from entryinfo WHERE BlogTitle = '" + blogtitle + "' ORDER BY EntryNum DESC;'")
            num = c.fetchone()
            for row in num:
                entrynum += row
            entrynum += 1
            c.execute("INSERT INTO entryinfo (BlogTitle, EntryNum, EntryTitle, Entry) VALUES (?,?,?,?)", (str(blogtitle),entrynum,str(entrytitle),str(entry)))
            db.commit()
            print("entry added")

            c = db.cursor()
            c.execute('SELECT EntryTitle, Entry FROM entryinfo WHERE BlogTitle = "' + blogtitle + '" ORDER BY EntryNum DESC;')
            entries = c.fetchall()
        return render_template("blog.html", BlogTitle = blogtitle, entries = entries)
    else :
        return "ERROR"



@app.route("/whereto", methods=['GET', 'POST'])
def whereto():
    if request.method == 'POST':
        blogtitle = request.form['whereto']
        with sqlite3.connect(DB_FILE) as db:
            c = db.cursor()
            c.execute('SELECT EntryTitle, Entry FROM entryinfo WHERE BlogTitle = "' + blogtitle + '" ORDER BY EntryNum DESC;')
            entries = c.fetchall()
        return render_template("blog.html", BlogTitle = blogtitle, entries = entries)
    else :
        return "ERROR"


def validate(name, value):
    error_message = ""
    if name == "userID":
        if value == "" or value == " " or value == None:
            error_message += " Username cannot be blank"
        if check_existence("username", value):
            error_message += " Username already exists"
        if len(value) > 50:
            error_message += " Username cannot exceed 50 characters"
    if name == "password":
        if len(value) < 1 or len(value) > 50:
            error_message += " Password must only have between 1 and 50 characters"
        if(value != request.args['cpass']):
            error_message += " Passwords must match"
    if name == "blogtitle":
        if value == "" or value == " " or value == None:
            error_message += " Blog Title cannot be blank"
        if len(value) < 1 or len(value) > 50:
            error_message += " Blog Title must only have between 1 and 50 characters"
    if name == "entrytitle":
        if value == "" or value == " " or value == None:
            error_message += " Entry Title cannot be blank"
        if len(value) < 1 or len(value) > 50:
            error_message += " Entry Title must only have between 1 and 50 characters"
    if name == "entry":
        if value == "" or value == " " or value == None:
            error_message += " Entry cannot be blank"
        if len(value) < 1 or len(value) > 50:
            error_message += " Entry must only have between 1 and 50 characters"
    return error_message

def check_existence(c_name, value):
    with sqlite3.connect(DB_FILE) as db:
        c = db.cursor()
        c.execute("SELECT " + c_name + " FROM userinfo WHERE " +c_name + " LIKE '%" + value + "%';")
        listUsers = c.fetchall()
        print(listUsers)
        if (len(listUsers) == 0):
            return False
        return True

@app.route("/logout", methods=['POST']) #Logout method
def logout():
    if len(session) > 0 and len(session.get("userID")) > 0: #If username does exist, remove it from session and return the login page
        session.pop("userID")
    return render_template('login.html', login_html = "")

@app.route('/',methods = ['GET','POST'])
def addrec():
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    db.execute('pragma foreign_keys=ON')
    c = db.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS userinfo (username TEXT, password TEXT, BlogID INTEGER PRIMARY KEY)")
    c.execute("CREATE TABLE IF NOT EXISTS bloginfo (BlogTitle TEXT, BlogID INTEGER, CONSTRAINT fk_userinfo FOREIGN KEY(BlogID) REFERENCES userinfo(BlogID))")
    c.execute("CREATE TABLE IF NOT EXISTS entryinfo (BlogTitle TEXT, EntryNum TEXT, EntryTitle TEXT, Entry TEXT)")

    print("***create table works***") #this creates a new table
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']

        except:
            print("error")
    print('***rendered templated***')
    return render_template('list.html')
@app.route('/list')
def list():
   con = sqlite3.connect(DB_FILE)
   con.row_factory = sqlite3.Row

   cur = con.cursor()
   cur.execute("select * from userinfo")

   rows = cur.fetchall()
   c = con.cursor()
   c.execute("select * from bloginfo")
   blog = c.fetchall()
   return render_template("list.html",rows = rows, blog = blog)

def insert(table_name, username, password): #insert user and password into table
    with sqlite3.connect(DB_FILE) as db:
            #open if file exists, otherwise create
            c = db.cursor()
            c.execute("INSERT INTO " + table_name + "(username,password) VALUES (?,?)",(username,password) )
            db.commit()
            msg = "Record successfully added"

def search(keyword):
    with sqlite3.connect(DB_FILE) as db:
        c = db.cursor()
        c.execute("SELECT BlogTitle, EntryID FROM bloginfo WHERE BlogTitle LIKE '%" + keyword + "%';")
        blogs = c.fetchall()
        print(blogs)
        return blogs

def show_entries(blog):
    with sqlite3.connect(DB_FILE) as db:
        c = db.cursor()
        c.execute('EntryTitle, Entry FROM entryinfo WHERE BlogTitle = "' + blog + '" ORDER BY EntryNum;')
        entries = c.fetchall()
        return render_template("blog.html", BlogTitle = blog, entries = entries)


if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
