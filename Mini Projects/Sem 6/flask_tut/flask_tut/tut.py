from flask import Flask, render_template, request, redirect,session,flash,url_for,g
from datetime import  timedelta
app=Flask(__name__)
import os
import mysql.connector

app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(minutes=5)
mydb=mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='',
    database = 'meditracker'
)

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user=session['user']
    print(g.user)


@app.route("/")
def home():
    return render_template('index.html')
@app.route("/about")
def about():
    return render_template('about.html')
@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        name=request.form.get('name')
        type = request.form.get('type')
        phone=request.form.get('phone')
        email=request.form.get('email')
        password=request.form.get('password')
        if(type=="admin"):
            query="insert into  signup(name,type,phone,email,password) VALUES (%s,%s,%s,%s,%s)"
            val = (name,type,phone,email,password)
            mycursor = mydb.cursor()
            mycursor.execute(query, val)
            mydb.commit()
            mydb.close()
    return render_template('contact.html')
@app.route("/login", methods=['GET','POST'])
def login():
    if(request.method=='POST'):
        session.pop('user', None)
        email=request.form.get('email')
        password=request.form.get('password')
        try:
            mycursor = mydb.cursor()
            mycursor.execute('SELECT * FROM signup WHERE email=%s and password=%s', (email,password))
            records = mycursor.fetchall()
            session['user'] = email
            # session.permanent = True
            if "user" in session :
                user = session['user']
            for row in records:
                type=str(row[1])
            if(type=='admin'):
                return render_template('admin.html',user=user)

            if(type=='patient'):
                return render_template('patient.html')
            if(type=='Doctor'):
                return render_template('doctor.html')
        except:
            print("Wrong emil password")
            flash("Wrong Details")
            return render_template("login.html")
    try:
        return render_template('login.html',user=user)
    except:
        return render_template('login.html')

@app.route('/admin')
def admin():
    if(g.user):
        return render_template('admin.html',user=session['user'])
    return render_template('login.html')

@app.route("/logout")
def logout():
    session.pop('user', None)
    return render_template('login.html')
app.run(debug=True)
