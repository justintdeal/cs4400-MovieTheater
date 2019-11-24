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
    else:


@app.route("/dashboard/")
def dashboard():
    types = ['Manager', 'Cust', 'Admin', 'User', 'AdminCust', 'ManagerCust']

    userType = types[4]
    template = "dash"+ userType +".html"
    return render_template(template)

@app.route("/manage/user", methods=['GET', 'POST'])
def manageUser():
    return render_template('manageUser.html')

@app.route("/manage/company", methods=['GET', 'POST'])
def manageCompany():
    return render_template('manageCompany.html')

@app.route("/manage/company/create/theater", methods=['GET', 'POST'])
def createTheater():
    return render_template('createTheater.html')

@app.route("/manage/company/<name>", methods=['GET', 'POST'])
def viewCompany(name):
    return render_template('viewCompany.html')

@app.route("/manage/company/create/movie", methods=['GET', 'POST'])
def createMovie():
    return render_template('createMovie.html')

@app.route("/manage/company/schedule/movie", methods=['GET', 'POST'])
def scheduleMovie():
    return render_template('scheduleMovie.html')

@app.route("/manage/company/theater/overview", methods=['GET', 'POST'])
def theaterOverview():
    return render_template('theaterOverview.html')

@app.route("/theater/explore", methods=['GET', 'POST'])
def exploreTheater():
    return render_template('exploreTheater.html')

@app.route("/movie/explore", methods=['GET', 'POST'])
def exploreMovie():
    return render_template('exploreMovie.html')

@app.route("/movie/history", methods=['GET', 'POST'])
def viewHistory():
    return render_template('viewHistory.html')

@app.route("/visit/history", methods=['GET', 'POST'])
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


def validateEmail(email):
    regx = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if (re.search(regx, email)):
        return True
    return False

def validatePass(password, confPass):
    return 0