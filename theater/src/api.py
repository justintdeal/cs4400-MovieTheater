from theater import app
import theater.src.procedureInterface as db
import theater.src.register as reg
from flask import render_template, request, url_for, redirect, json

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
            message = "Invalid Login"
            return render_template('home.html', messages=message)
        user=user[0]
        return redirect(url_for('dashboard', user = user))

#screen 2
@app.route("/register")
def regiserHome():
    return render_template('registerHome.html')

#screens 3-6
# populate company dropdown
@app.route("/register/<role>", methods=['GET', 'POST'])
def registerRole(role):
    if request.method == 'GET':
        return reg.getRegTemplate(role)
    else:
        return reg.register(role)

#screens 7-12
@app.route("/dashboard/")
def dashboard(user):
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
