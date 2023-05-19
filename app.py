from flask import Flask, render_template, request, redirect,url_for
import ibm_db
import ibm_boto3
from ibm_botocore.client import Config, ClientError
import os

app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=19af6446-6171-4641-8aba-9dcff8e1b6ff.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30699;SECURITY=SSL;./SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=dqh38066;PWD=jVyOCXpJPG3M3r81",'','')
useremail=''
cos_endpoint="https://s3.jp-tok.cloud-object-storage.appdomain.cloud"
cos_apikey="YIslPTOvNe3j0DRZj5ePHEfLmrtApQsavLSt9IoSELMn"
cos_crn="crn:v1:bluemix:public:cloud-object-storage:global:a/4ba25fea32e046cdb8e6cbe2ad24f6ca:d144147f-700e-491b-b7d6-c07c8ba51fa2::"
cos=ibm_boto3.client('s3',ibm_api_key_id=cos_apikey,ibm_service_instance_id=cos_crn,endpoint_url=cos_endpoint,config= Config(signature_version="oauth"))
 
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
            ibm_db.bind_param(stmt,1,str(username))
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
    global useremail
    if request.method=="POST":
        check=True
        email=request.form['email']
        useremail=email.lower()
        password=request.form['pswd']
        if useremail=="admin@123.com" and password=="admin":
            return render_template("homeadmin.html")
        sql = "SELECT * FROM TEST"
        stmt = ibm_db.exec_immediate(conn, sql)
        dictionary = ibm_db.fetch_both(stmt)
        while dictionary != False:
            if useremail==dictionary[1] and password==dictionary[2]:
                check=False
                break
            dictionary = ibm_db.fetch_both(stmt)
        if check==True:
            msg="Incorrect Username or Password"
            msgb="Click to Try again"
            return render_template('regerror.html',msg=msg,msgb=msgb)
        else:
            return redirect(url_for("home"))



@app.route('/home')
def home():
    if useremail=='':
        return render_template("reg.html")
    else:
        return render_template("homepage.html")

@app.route('/upload',methods=['GET','POST'])
def upload():
    if useremail!='':
        return render_template('upload.html')
    else:
        return render_template("homepage.html")

@app.route('/page',methods=['GET','POST'])
def page():
    if useremail=="admin@123.com":
        return render_template('homeadmin.html')
    else:
        return render_template('reg.html')

@app.route('/admin',methods=['GET','POST'])
def admin():
    if useremail=="admin@123.com":
        sql = "SELECT * FROM UPLOADTEST"
        stmt = ibm_db.exec_immediate(conn, sql)
        data = ibm_db.fetch_both(stmt)
        i=0
        email = []
        title = []
        context = []
        id = []
        baselink = "https://test2504.s3.jp-tok.cloud-object-storage.appdomain.cloud/"
        link = []
        while data != False:
            id.insert(i, data[0])
            title.insert(i, data[1])
            context.insert(i, data[2])
            email.insert(i, data[3])
            link.insert(i, baselink+data[0]+".jpg")
            i=i+1
            data = ibm_db.fetch_both(stmt)
        return render_template('admin.html',id=id,title=title,context=context,email=email,len=len(id),link=link)
    else:
        return render_template("reg.html")

@app.route('/complaints',methods=['GET','POST'])
def complaints():
    sql = "SELECT * FROM UPLOADTEST"
    stmt = ibm_db.exec_immediate(conn, sql)
    data = ibm_db.fetch_both(stmt)
    i=0
    email = []
    title = []
    context = []
    id = []
    baselink = "https://test2504.s3.jp-tok.cloud-object-storage.appdomain.cloud/"
    link = []
    while data != False:
        if useremail==data[3]:
            id.insert(i, data[0])
            title.insert(i, data[1])
            context.insert(i, data[2])
            email.insert(i, data[3])
            link.insert(i, baselink+data[0]+".jpg")
        i=i+1
        data = ibm_db.fetch_both(stmt)
    return render_template('complaints.html',id=id,title=title,context=context,email=email,len=len(id),link=link)


@app.route('/home',methods=['GET','POST'])
def uploadfile():
    if request.method=="POST":
        check=True
        title=request.form['title']
        caption=request.form['caption']
        file = request.files['images']
        sql  = "SELECT MAX(ID) FROM UPLOADTEST"
        stmt = ibm_db.exec_immediate(conn, sql)
        idlist = ibm_db.fetch_tuple(stmt)
        if idlist==False:
            img_ID=1
        else:
            img_ID=int(max(idlist))+1
        fname=str(img_ID)
        file.save(fname)
        sql  = "INSERT INTO UPLOADTEST VALUES (?,?,?,?)"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,str(img_ID))
        ibm_db.bind_param(stmt,2,str(title))
        ibm_db.bind_param(stmt,3,str(caption))
        ibm_db.bind_param(stmt,4,str(useremail))
        ibm_db.execute(stmt)
        cos.upload_file(Filename = fname, Bucket = "test2504", Key = str(img_ID)+".jpg")
        path = "./"+fname
        os.remove(path)
        return render_template('homepageau.html')

if __name__=='__main__':
    app.run(host='0.0.0.0', debug=True)
