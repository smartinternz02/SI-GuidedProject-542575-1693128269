from flask import Flask, render_template,request,session
global uname
import ibm_db
app = Flask(__name__)
app.secret_key ="_ab+d=5"
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=2f3279a5-73d1-4859-88f0-a6c3e6b4b907.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;port=30756;UID=trz14487;pwd=qOnA59D0cOFc1qLY;SECURITY=SSL;SSLCERTIFICATE=DigiCertGlobalRootCA.crt",'','')
print(ibm_db.active(conn))
@app.route("/")
def index():
 return render_template("index.html")
@app.route("/contact")
def contact():
 return render_template("contact.html")
@app.route("/login",methods=["GET","POST"])
def login():
  if request.method == "POST":
    uname = request.form["username"]
    pword = request.form["password"]
    print (uname,pword)
    sql = "SELECT * FROM REGISTER_KLU WHERE USERNAME= ? AND PASSWORD=?"
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,uname)
    ibm_db.bind_param(stmt,2,pword)
    ibm_db.execute(stmt)
    # ibm_db.fetch_assoc(stmt)
    out = ibm_db.fetch_assoc(stmt)
    print(out)
    if out !=False:
      session['username'] = uname
      session['emilid'] =out['EMAIL ID']
      if out['ROLE'] ==0:
        return render_template ("adminprofile.html",username=uname,emailid = out['EMAIL ID'])
      elif out['ROLE'] ==1:
        return render_template("studentprofile.html",username=uname,emailid = out['EMAIL ID'])
      else:
        return render_template("facultyprofile.html",username=uname,emailid = out['EMAIL ID'])
    else:
      msg="Invalid Credential"
      return render_template("login.html",message1 = msg)
  return render_template("login.html")
@app.route("/register",methods=['GET','POST'])
def register():
  if request.method == "POST":
    uname=request.form['sname']
    email=request.form['semail']
    pword=request.form['spassword']
    role=request.form['role']
    print(uname,email,pword,role)
    sql="SELECT * FROM REGISTER_KLU WHERE USERNAME= ?"
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,uname)
    ibm_db.execute(stmt)
    out=ibm_db.fetch_assoc(stmt)
    print(out)
    if out !=False:
      msg="Already Registered"
      return render_template("register.html",msg=msg)
    else:
      sql="INSERT INTO REGISTER_KLU VALUES(?,?,?,?)" 
      stmt = ibm_db.prepare(conn,sql)
      ibm_db.bind_param(stmt,1,uname)
      ibm_db.bind_param(stmt,1,pword)
      ibm_db.bind_param(stmt,1,email)
      ibm_db.bind_param(stmt,1,role)
      ibm_db.execute(stmt)
      return render_template("register.html",msg=msg)
  return render_template("register.html")
if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
    