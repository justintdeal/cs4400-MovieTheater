from theater import app
import theater.src.dbConnection as db
from flask import render_template, request, flash, url_for, redirect

#screen 1: login
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        user = request.form['email']
        password = request.form['password']
        #user (username, status, isCustomer, isAdmin, isManager)
        user = db.userLogin(user, password)
        if user[0] == None:
            flash('Invalid Login')
            return render_template('home.html')
        user=user[0]
        return redirect(url_for('dashboard', user = user))

#screen 2
@app.route("/register")
def regiserHome():
    return render_template('registerHome.html')

#screens 3-6

# unique credit card numbers
# # credit card >=1 && <=5 and lenght == 16
# populate company dropdown
@app.route("/register/<role>", methods=['GET', 'POST'])
def registerRole(role):
    if request.method == 'GET':
        return getRegTemplate(role)
    else:
        if role == "user":
            password = request.form['password']
            confPass = request.form['confPass']
            first = request.form['first']
            last = request.form['last']
            username = request.form['username']
    
            if password == confPass and len(password) >= 8:
                db.userRegister(username, password, first, last)
            elif len(password) <= 8:
                print(10)
                message = "Password must be at least 8 characters"
                return render_template("userReg.html", messages=message)
            else:
                message = "Passwords must match"
                return getRegTemplate("user", message)
        if role == "customer":
            password = request.form['password']
            confPass = request.form['confPass']
            first = request.form['first']
            last = request.form['last']
            username = request.form['username']
            return "hello"


def getRegTemplate(role, messages=None):
    if role == 'user':
        return render_template('userReg.html', messages=messages)
    elif role == "manager":
        return render_template('manReg.html', messages=messages)
    elif role == "customer":
        return render_template('custReg.html', messages=messages)
    elif role == "mancust":
        return render_template('custManReg.html', messages=message)

#screens 7-12
@app.route("/dashboard/")
def dashboard(user):
    #user (username, status, isCustomer, isAdmin, isManager)
    userType = getUserType(user)
    template = "dash"+ userType +".html"
    return render_template(template)

def getUserType(user):
    if user[3] and not user[2] and not user[4]:
        return "Admin"
    if user[3] and user[2] and not user[4]:
        return "AdminCust"
    if user[4] and not user[2] and not user[3]:
        return "Manager"
    if user[2] and user[4] and not user[3]:
        return "ManagerCust"
    if user[2] and not user[4] and not user[3]:
        return "Customer"
    return "User"

#screen 13
# can approve pending/declined users
# can decline pending
# cannot decline approve
@app.route("/manage/user", methods=['GET', 'POST'])
def manageUser():
    return render_template('manageUser.html')

#screen 14
# can search theaters by #cities coverd, #theaters, and #Employee
# make name dropdown menu
# inclusive searches
@app.route("/manage/company", methods=['GET', 'POST'])
def manageCompany():
    return render_template('manageCompany.html')

#screen 15: Admin Create Theater
# populate company
# name for theater is unique for theaters within a company
# theater must be managed by existing non assigned managers
@app.route("/manage/company/create/theater", methods=['GET', 'POST'])
def createTheater():
    return render_template('createTheater.html')

#screen 16: Admin Company Detail
@app.route("/manage/company/<name>", methods=['GET', 'POST'])
def viewCompany(name):
    return render_template('viewCompany.html')

#screen 17: Admin Create Movie
# standardize release date
@app.route("/manage/company/create/movie", methods=['GET', 'POST'])
def createMovie():
    return render_template('createMovie.html')

#
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
