# BlueGreen (Edwin Zheng, Shriya Anand, Zhaoyu Lin)
# SoftDev
# K16: All About Database
# Oct 22, 2021

import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O


DB_FILE="discobandit.db" #this is the original file

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

#==========================================================

c.execute("CREATE TABLE roster (name TEXT, age INTEGER, id INTEGER) ") #this creates a new table

with open('students.csv') as csvfile: #this opens the students data
    reader = csv.reader(csvfile, delimiter= ",") #this splits the data on commas
    for row in reader:
        name = row[0] #each row is split into a list
        age = row[1]
        id = row[2]
        if(age != "age"): #gets rid of heading line
            command = "INSERT INTO roster VALUES ('" + name + "'," + age + "," + id + ")" #added single quotes for the text for sql
            c.execute(command);

# same things but for courses.csv instead
c.execute("CREATE TABLE classes (code TEXT, mark INTEGER, id INTEGER)")
with open('courses.csv') as file:
    r = csv.reader(file, delimiter= ",")
    for row in r:
        code = row[0]
        mark = row[1]
        id = row[2]
        if(mark != "mark"):
            command = "INSERT INTO classes VALUES ('" + code + "'," + mark + "," + id + ")"
            c.execute(command);

#==========================================================

db.commit() #save changes
db.close()  #close database
