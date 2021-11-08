# BlueGreen (Edwin Zheng, Shriya Anand, Zhaoyu Lin)
# SoftDev
# K15: Sessions Greetings
# Oct 20, 2021

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
        return render_template('response.html', user = session.get("userID")) #return response page if correct user name is stored in session

@app.route("/auth", methods=['GET', 'POST'])
def authenticate():
    username = "Traveler"
    password = "12345"
    response = "TRY AGAIN: "

    if(request.args['username'] != username): #check if username is correct
        response += "incorrect username --- "
    if(request.args['password'] != password): #check if password is correct
        response += "incorrect password ---"

    if(response == "TRY AGAIN: "):  #If the username and password is correct, return response.html with the Username, store in database
        session["userID"] = request.args['username']
        insert("userinfo", request.args['username'], request.args['password'])
        print("************************" + session["userID"])



        return render_template('response.html', user = session.get("userID"))
    return render_template('login.html', login_fail = response) #Else, return the response telling you what's wrong

@app.route("/reg1", methods=['GET', 'POST'])
def reg1():
    return render_template('register.html')

@app.route("/reg2", methods=['GET', 'POST'])
def reg2():
    error = "ERROR: "
    if (request.args['regUser'] == "Traveler"):
        error += "Pre-existing username. Please choose a different username"
    if (len(request.args['regUser']) == 0 or len(request.args['regPass']) == 0):
        error += "Empty field. Please fill out the fields"

    if (error == "ERROR: "):
        #if userID is valid, store in database
        session["userID"] = request.args['regUser']
        insert("userinfo", request.args['regUser'], request.args['regPass'])
        print("************************" + session["userID"])
        return render_template('response.html',user = request.args['regUser'])
            # ADD USERID TO THE DB HERE

    return render_template('register.html', error = error)
    # return render_template('response.html', user = session.get("userID"))

def check_existence(table_name, value):
    #check if user exists in DB
    #arg = tablename,
@app.route("/logout", methods=['POST']) #Logout method
def logout():
    if session.get("userID") == "Traveler": #If username does exist, remove it from session and return the login page
        session.pop(session[-1])
    return render_template('login.html', login_html = "")

@app.route('/',methods = ['GET','POST'])
def addrec():
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()
    c.execute("DROP TABLE IF EXISTS userinfo")
    c.execute("CREATE TABLE userinfo (username TEXT, password TEXT)")
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

   rows = cur.fetchall();
   return render_template("list.html",rows = rows)

def insert(table_name, username, password):#insert user and password into table
    with sqlite3.connect(DB_FILE) as db:
            #open if file exists, otherwise create
            c = db.cursor()
            c.execute("INSERT INTO " + table_name + "(username,password) VALUES (?,?)",(username,password) )

            db.commit()
            msg = "Record successfully added"

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
