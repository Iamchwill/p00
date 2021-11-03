# BlueGreen (Edwin Zheng, Shriya Anand, Zhaoyu Lin)
# SoftDev
# K15: Sessions Greetings
# Oct 20, 2021

from flask import Flask, render_template, request, session     #facilitate flask webservingimport
import os

app = Flask(__name__)    #create Flask object
app.secret_key = os.urandom(32) #create random key

@app.route("/") #,methods=['GET', 'POST'])
def disp_loginpage():
    response = ""
    if "userID" not in session: #check if there is the correct user name stored in session
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

    if(response == "TRY AGAIN: "):  #If the username and password is correct, return response.html with the Usernamet
        session["userID"] = request.args['username']
        return render_template('response.html', user = session.get("userID"))
    return render_template('login.html', login_fail = response) #Else, return the response telling you what's wrong

@app.route("/reg", methods=['GET', 'POST'])
def register():
     return render_template('register.html')

@app.route("/logout", methods=['POST']) #Logout method
def logout():
    if session.get("userID") == "Traveler": #If username does exist, remove it from session and return the login page
        session.pop("userID")
    return render_template('login.html', login_html = "")


if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
