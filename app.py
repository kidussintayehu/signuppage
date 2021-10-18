from flask import Flask,render_template,request
import sqlite3
import hashlib
import re

app=Flask(__name__)

connection=sqlite3.connect("store.db")

db=connection.cursor()


db.execute("""CREATE TABLE IF NOT EXISTS airlines(
    flight_id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(50) NOT NULL,
    day DATE NOT NULL);
    """)

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/registor page")
def registor_page():
    return render_template("registor.html")
@app.route("/login page")
def login_page():
    return render_template("login.html")
@app.route("/registor",methods=['[POST]','[GET]'])
def registor():
    name=request.form["name"]
    password=request.form["password"]
    day=request.form["day"]
    hashed_password=hashlib.sha256(str(password).encode('utf-8')).hexdigest()
    conn=sqlite3.connect("store.db")
    db=conn.cursor()
    
    nameTuple=(name, )
    passwordTuple=(hashed_password, )
    name_query="SELECT * FROM airlines WHERE name=?"
    password_query="SELECT * FROM airlines WHERE password=?"
    db.execute(name_query,nameTuple)
    db.execute(password_query,passwordTuple)
    
    record=db.fetchall()
    
    for row in record:
        if row[1]==name and row[2]==hashed_password:
            return "u already have acount"
    if name=="" or day=="":
        return "u missed to type name or day "
    regexNameForAlphabets=re.findall("[a-zA-Z]",name)
    regexNameForDigits=re.findall("\d",name)
    if regexNameForAlphabets and regexNameForDigits:
        insert_query="INSERT INTO airlines(name,password,day) VALUES(?,?,?)"
        db.execute(insert_query,(name,hashed_password,day))
        conn.commit()
        db.close()
        return render_template("registered.html")
    return "you have to use alphabets and numbers only"
   

@app.route("/login",methods=["POST"])
def login():
    
    name=request.form["name"]
    password=request.form["password"]
    password=hashlib.sha256(str(password).encode('utf-8')).hexdigest()
    
    con=sqlite3.connect("store.db")
    con=con.cursor()
    query="SELECT * FROM airlines WHERE name=%s"
    query1="SELECT * FROM airlines WHERE password=%s"
    con.execute(query,name)
    con.execute(query1,password)
    
    record=con.fetchall()
    
    for row in record:
        if row[1]==name and row[2]==password:
            return render_template("reminder.html",name=row[1])
        
    return "sth mismatch"
    
@app.route("/reminder")
def reminder():
    return render_template("reminder.html")

@app.route("/registered")
def registered():
    return render_template("registered.html")