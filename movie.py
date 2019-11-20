from flask import Flask, render_template, request

app = Flask(__name__)

#This is where the user will login
#if get show login form if post show validate login
#users can also go to register pages from here
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        return "hello"

@app.route("/register")
def regiserHome():
    return render_template('registerHome.html')

@app.route("/register/<role>", methods=['GET', 'POST'])
def registerRole(role):
    if request.method == 'GET':
        return getRegTemplate(role)

@app.route("/dashboard/")
def dashboard():
    types = ['Man', 'Cust', 'Admin', 'User', 'AdminCust', 'ManCust']

    userType = types[3]
    template = "dash"+ userType +".html"
    return render_template(template)

@app.route("/manage/user")
def manageUser():
    return render_template('manageUser.html')

@app.route("/manage/company")
def manageCompany():
    return render_template('manageCompany.html')



#helpers
def getRegTemplate(role):
    if role == 'user':
        return render_template('userReg.html')
    elif role == "manager":
        return render_template('manReg.html')
    elif role == "customer":
        return render_template('custReg.html')
    elif role == "mancust":
        return render_template('custManReg.html')




