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
    userType = "Base"
    template = "dash"+ userType +".html"
    
    #dashMan
    #dashCust
    #dashAdmin
    #dashUser
    #dashAdminCust
    #dashManCust
    print(userType)
    return render_template(template)

@app.route("/dashboard/admin")
def adminDashboard():
    return render_template('dashAdmin.html')

@app.route("/dashboard/adminCust")
def adminCustDashboard():
    return render_template('dashAdminCust.html')

@app.route("/dashboard/manager")
def managerDashboard():
    return render_template('dashManager.html')

@app.route("/dashboard/managerCust")
def managerCustDashboard():
    return render_template('dashManagerCust.html')

@app.route("/dashboard/customer")
def customerDashboard():
    return render_template('dashCustomer.html')

@app.route("/dashboard/user")
def userDashboard():
    return render_template('dashUser.html')

@app.route("/manage/user")
def manageUser():
    return render_template('manageUser.html')

@app.route("/manage/company")
def manageCompany():
    return render_template('manageCompany.html')

@app.route("/manage/company/create/theater")
def createTheater():
    return render_template('createTheater.html')

@app.route("/manage/company/<name>")
def viewCompany(name):
    return render_template('viewCompany.html')

@app.route("/manage/company/create/movie")
def createMovie():
    return render_template('createMovie.html')

@app.route("/manage/company/schedule/movie")
def scheduleMovie():
    return render_template('scheduleMovie.html')

@app.route("/manage/company/theater/overview")
def theaterOverview():
    return render_template('theaterOverview.html')

@app.route("/theater/explore")
def exploreTheater():
    return render_template('exploreTheater.html')

@app.route("/movie/explore")
def exploreMovie():
    return render_template('exploreMovie.html')

@app.route("/movie/history")
def viewHistory():
    return render_template('viewHistory.html')

@app.route("/visit/history")
def visitHistory():
    return render_template('visitHistory.html')



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




