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
        query="insert into  signup(name,type,phone,email,password) VALUES (%s,%s,%s,%s,%s)"
        val = (name,type,phone,email,password)
        mycursor = mydb.cursor()
        mycursor.execute(query, val)
        mydb.commit()
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
                return redirect(url_for('admin'))
            if(type=='patient'):
                return redirect(url_for('patient'))
            if(type=='doctor'):
                return redirect(url_for('doctor'))
        except:
            print("Wrong email or password")
            flash("Wrong Details")
            return render_template("login.html")
    try:
        return render_template('login.html',user=user)
    except:
        return render_template('login.html')
@app.route('/admin')
def admin():
    if(g.user):
        return render_template('admin1.html',user=session['user'])
    return render_template('login.html')
@app.route('/addrec')
def addrec():
    if "user" in session :
        user = session['user']
    return render_template('add.html',user=user)
@app.route('/addrecpost', methods=['POST','GET'])
def addrecpost():
    if 'user' in session:
        user = session['user']
    if (request.method == 'POST') :
        name=request.form.get('name')
        email=request.form.get('email')
        dob=request.form.get('dob')
        gender=request.form.get('gender')
        contact=request.form.get('contact')
        medical=request.form.get('medical')
        print("1")
        query = "insert into  addreco(name,email,dob,gender,contact,medical) VALUES (%s,%s,%s,%s,%s,%s)"
        val = (name,email, dob, gender, contact, medical)
        mycursor = mydb.cursor()
        mycursor.execute(query, val)
        print("2")
        mydb.commit()
    return render_template('add.html')
@app.route("/viewrec",methods=['POST','GET'])
def view():
    if 'user' in session :
        user = session['user']
    if (request.method == 'POST') :

        try:
            email=request.form.get("email")
            mycursor=mydb.cursor()
            mycursor.execute('SELECT * FROM addreco WHERE email=%s',(email,))
            myresult=mycursor.fetchall()
            for x in myresult:
                print(x)
            mydb.commit()
        except:
            render_template('view.html',user=user)
    try:
        return render_template('view.html',data=myresult,user=user)
    except:
        return render_template('view.html',  user=user)
@app.route("/editrec",methods=['POST','GET'])
def edit():
    if 'user' in session :
        user = session['user']
    if (request.method == 'POST') :

        try:
            email=request.form.get("email")
            mycursor=mydb.cursor()
            mycursor.execute('SELECT * FROM addreco WHERE email=%s',(email,))
            myresult=mycursor.fetchall()
            for x in myresult:
                print(x)
            mydb.commit()
        except:
            render_template('edit.html',user=user)
    try:
        return render_template('edit.html',data=myresult,user=user)
    except:
        return render_template('edit.html',  user=user)
@app.route('/update')
def upd():
    if(g.user):
        return render_template('update.html',user=session['user'])
    return render_template('update.html')
@app.route('/updaterec', methods=['POST', 'GET'])
def update():
    if request.method=='POST':
            name=request.form.get('name')
            email=request.form.get('email')
            dob=request.form.get('dob')
            gender=request.form.get('gender')
            contact=request.form.get('contact')
            medical=request.form.get('medical')
            cur=mydb.cursor()
            cur.execute(""" UPDATE addreco SET name=%s, email=%s, dob=%s, gender=%s, contact=%s, medical=%s """,(name,email,dob,gender,contact,medical))
            flash("DATA UPDATED SUCCESSFULLY")
            mydb.commit()
    return render_template('edit.html')
@app.route("/viewsch",methods=['POST','GET'])
def viewsch():
    if 'user' in session :
        user = session['user']
    if (request.method == 'POST') :

        try:
            docname=request.form.get("docname")
            mycursor=mydb.cursor()
            mycursor.execute('SELECT * FROM schedule WHERE docname=%s',(docname,))
            myresult=mycursor.fetchall()
            for x in myresult:
                print(x)
            mydb.commit()
        except:
            render_template('viewsch.html',user=user)
    try:
        return render_template('viewsch.html',data=myresult,user=user)
    except:
        return render_template('viewsch.html',  user=user)
@app.route('/doctor')
def doctor():
    if(g.user):
        return render_template('doctor1.html',user=session['user'])
    return render_template('login.html')
@app.route("/viewrecd",methods=['POST','GET'])
def view2():
    if 'user' in session :
        user = session['user']
    if (request.method == 'POST') :

        try:
            email=request.form.get("email")
            mycursor=mydb.cursor()
            mycursor.execute('SELECT * FROM addreco WHERE email=%s',(email,))
            myresult=mycursor.fetchall()
            for x in myresult:
                print(x)
            mydb.commit()
        except:
            render_template('viewd.html',user=user)
    try:
        return render_template('viewd.html',data=myresult,user=user)
    except:
        return render_template('viewd.html',  user=user)
@app.route("/editrecd",methods=['POST','GET'])
def edit1():
    if 'user' in session :
        user = session['user']
    if (request.method == 'POST') :

        try:
            email=request.form.get("email")
            mycursor=mydb.cursor()
            mycursor.execute('SELECT * FROM addreco WHERE email=%s',(email,))
            myresult=mycursor.fetchall()
            for x in myresult:
                print(x)
            mydb.commit()
        except:
            render_template('editd.html',user=user)
    try:
        return render_template('editd.html',data=myresult,user=user)
    except:
        return render_template('editd.html',  user=user)
@app.route('/update1')
def upd1():
    if(g.user):
        return render_template('updated.html',user=session['user'])
    return render_template('updated.html')
@app.route('/updaterecd', methods=['POST', 'GET'])
def update1():
    if request.method=='POST':
            name=request.form.get('name')
            email=request.form.get('email')
            dob=request.form.get('dob')
            gender=request.form.get('gender')
            contact=request.form.get('contact')
            medical=request.form.get('medical')
            cur=mydb.cursor()
            cur.execute(""" UPDATE addreco SET name=%s, email=%s, dob=%s, gender=%s, contact=%s, medical=%s """,(name,email,dob,gender,contact,medical))
            flash("DATA UPDATED SUCCESSFULLY")
            mydb.commit()
    return render_template('editd.html')
@app.route('/addsched', methods=['POST','GET'])
def addsc():
    if 'user' in session:
        user = session['user']
    if (request.method == 'POST') :
        docname=request.form.get('docname')
        day=request.form.get('day')
        time=request.form.get('time')
        query = "insert into  schedule(docname,day,time) VALUES (%s,%s,%s)"
        val = (docname,day,time)
        mycursor = mydb.cursor()
        mycursor.execute(query, val)
        mydb.commit()
    return render_template('addsch.html')
@app.route("/viewapp",methods=['POST','GET'])
def viewapp():
    if 'user' in session :
        user = session['user']
    if (request.method == 'POST') :

        try:
            docname=request.form.get("docname")
            mycursor=mydb.cursor()
            mycursor.execute('SELECT * FROM appointment WHERE docname=%s',(docname,))
            myresult=mycursor.fetchall()
            for x in myresult:
                print(x)
            mydb.commit()
        except:
            render_template('viewap.html',user=user)
    try:
        return render_template('viewap.html',data=myresult,user=user)
    except:
        return render_template('viewap.html',  user=user)
@app.route('/patient')
def patient():
    if(g.user):
        return render_template('patient1.html',user=session['user'])
    return render_template('login.html')
@app.route("/viewrecp",methods=['POST','GET'])
def view1():
    if 'user' in session :
        user = session['user']
    if (request.method == 'POST') :

        try:
            email=request.form.get("email")
            mycursor=mydb.cursor()
            mycursor.execute('SELECT * FROM addreco WHERE email=%s',(email,))
            myresult=mycursor.fetchall()
            for x in myresult:
                print(x)
            mydb.commit()
        except:
            render_template('viewp.html',user=user)
    try:
        return render_template('viewp.html',data=myresult,user=user)
    except:
        return render_template('viewp.html',  user=user)
@app.route("/viewschp",methods=['POST','GET'])
def viewschp():
    if 'user' in session :
        user = session['user']
    if (request.method == 'POST') :

        try:
            docname=request.form.get("docname")
            mycursor=mydb.cursor()
            mycursor.execute('SELECT * FROM schedule WHERE docname=%s',(docname,))
            myresult=mycursor.fetchall()
            for x in myresult:
                print(x)
            mydb.commit()
        except:
            render_template('viewps.html',user=user)
    try:
        return render_template('viewps.html',data=myresult,user=user)
    except:
        return render_template('viewps.html',  user=user)
@app.route('/bookapp', methods=['POST','GET'])
def bookapp():
    if 'user' in session:
        user = session['user']
    if (request.method == 'POST') :
        name=request.form.get('name')
        emailid=request.form.get('emailid')
        docname=request.form.get('docname')
        day=request.form.get('day')
        time=request.form.get('time')
        print("1")
        query = "insert into  appointment(name,emailid,docname,day,time) VALUES (%s,%s,%s,%s,%s)"
        val = (name,emailid, docname, day, time)
        mycursor = mydb.cursor()
        mycursor.execute(query, val)
        print("2")
        mydb.commit()
    return render_template('book.html')
@app.route("/logout")
def logout():
    session.pop('user', None)
    return render_template('login.html')
app.run(debug=True)