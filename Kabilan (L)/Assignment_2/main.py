from flask import Flask, render_template, request, redirect,url_for
import ibm_db


app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=19af6446-6171-4641-8aba-9dcff8e1b6ff.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30699;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=dqh38066;PWD=jVyOCXpJPG3M3r81",'','')
 
 
@app.route('/reg',methods=['GET','POST'])
@app.route('/',methods=['GET','POST'])
def index():
    return render_template('reg.html')


@app.route('/sign',methods=['GET','POST'])
def signup():
    if request.method=="POST":
        check=True
        name=request.form['txt']
        name=name.lower()
        email=request.form['email']
        email=email.lower()
        password=request.form['pswd']
        sql = "SELECT * FROM TEST"
        stmt = ibm_db.exec_immediate(conn, sql)
        dictionary = ibm_db.fetch_both(stmt)
        msgb=""
        while dictionary != False:
            if email==dictionary[1]:
                check=False
                msg="Already Registered"
                msgb="Click to Login"
                break
            dictionary = ibm_db.fetch_both(stmt)
        if check==True:
            sql  = "INSERT INTO TEST VALUES (?,?,?)"
            stmt = ibm_db.prepare(conn,sql)
            ibm_db.bind_param(stmt,1,str(name))
            ibm_db.bind_param(stmt,2,str(email))
            ibm_db.bind_param(stmt,3,str(password))
            ibm_db.execute(stmt)
            msgb="Click here to Login"
            msg="Successfully Registered"
            return render_template('regerror.html',msg=msg,msgb=msgb)
        else:
            return render_template('regerror.html',msg=msg,msgb="Click to Login")

@app.route('/log',methods=['GET','POST'])
def login():
    if request.method=="POST":
        check=True
        email=request.form['email']
        password=request.form['pswd']
        sql = "SELECT * FROM TEST"
        stmt = ibm_db.exec_immediate(conn, sql)
        dictionary = ibm_db.fetch_both(stmt)
        while dictionary != False:
            if email==dictionary[1] and password==dictionary[2]:
                check=False
                break
            dictionary = ibm_db.fetch_both(stmt)
        if check==True:
            msg="Incorrect Username or Password"
            msgb="Click to Try again"
            return render_template('regerror.html',msg=msg,msgb=msgb)
        else:
            msg="Logged in"
            return redirect(url_for("home"))


@app.route('/home')
def home():
    return "<h1>Homepage<h1>"

 
if __name__=='__main__':
    app.run(debug = True)
    
