from sqlite3.dbapi2 import Date
from flask import Flask,render_template,request
import sqlite3
import hashlib
from string import printable,ascii_letters,digits

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
@app.route("/registor",methods=['POST'])
def registor():
    name=request.form["name"]
    password=request.form["password"]
    day=request.form["day"]
    hashed_password=hashlib.sha256(str(password).encode('utf-8')).hexdigest()
    conn=sqlite3.connect("store.db")
    db=conn.cursor()
    print(name)
    print(hashed_password)
    print(day)
    print(day=="")
    nameTuple=(name, )
    passwordTuple=(hashed_password, )
    name_query="SELECT * FROM airlines WHERE name=?"
    password_query="SELECT * FROM airlines WHERE password=?"
    db.execute(name_query,nameTuple)
    db.execute(password_query,passwordTuple)
    
    record=db.fetchall()
    
    for row in record:
        # print(row[0])
        # print(row[1])
        # print(row[2])
        # print(row[3])
        # print(row[1]==name)
        # print(row[2]==password)
        if row[1]==name and row[2]==hashed_password:
            return "u already have acount"
    if name=="" or day=="":
        return "u missed to type name or day "
    print(set(name).difference(ascii_letters+digits))
    if set(name).difference(ascii_letters+digits):
        return "u used special charactor"
    insert_query="INSERT INTO airlines(name,password,day) VALUES(?,?,?)"
    db.execute(insert_query,(name,hashed_password,day))
    conn.commit()
    db.close()
    return render_template("registered.html")

@app.route("/login",methods=["POST"])
def login():
    
    name=request.form["name"]
    password=request.form["password"]
    password=hashlib.sha256(str(password).encode('utf-8')).hexdigest()
    print(name)
    print(password)
    con=sqlite3.connect("store.db")
    con=con.cursor()
    query="SELECT * FROM airlines WHERE name=%s"
    query1="SELECT * FROM airlines WHERE password=%s"
    con.execute(query,name)
    con.execute(query1,password)
    
    record=con.fetchall()
    
    for row in record:
        # print(row[0])
        # print(row[1])
        # print(row[2])
        # print(row[3])
        print(row[1]==name)
        print(row[2]==password)
        if row[1]==name and row[2]==password:
            return render_template("reminder.html",name=row[1])
        
    return "sth mismatch"
    
@app.route("/reminder")
def reminder():
    return render_template("reminder.html")

@app.route("/registered")
def registered():
    return render_template("registered.html")