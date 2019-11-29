from theater import app
import theater.src.procedureInterface as db
import theater.src.register as reg
from flask import render_template, request, url_for, redirect, session



#login stuff
@app.route('/logout')
def logout():
    session['active'] = False
    return render_template('home.html')

def loggedIn():
    try:
        return session['active']
    except:
        return False

#screen 1: login
@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        if loggedIn():
            return redirect(url_for('dashboard'))
        return render_template('home.html')
    else:
        user = request.form['email']
        password = request.form['password']
        #user (username, status, isCustomer, isAdmin, isManager)
        user = db.userLogin(user, password)
        if len(user) == 0:
            message = "Invalid Login: Wrong Credentials"
            return render_template('home.html', messages=message)
        if user[0][1] == 'declined':
            message = "Invalid Login: Declined User! Contact an Admin"
            return render_template('home.html', messages=message)
        print(user[0][1])
        user = user[0]
        session['active'] = True
        session['user'] = user[0]
        session['type'] = getUserType(user)
        print(session)
        return redirect(url_for('dashboard', user = user))

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

#screen 2
@app.route("/register")
def registerHome():
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
def dashboard():
    if not loggedIn():
        return redirect(url_for('index'))
    template = "dash"+ session['type'] + ".html"
    return render_template(template)



#screen 13
# can approve pending/declined users
# can decline pending
# cannot decline approve
@app.route("/manage/user", methods=['GET', 'POST'])
def manageUser():
    if not loggedIn():
        return redirect(url_for('index'))
    name = ''
    status = 'ALL'
    sortby = ''
    sortdir = ''
    #view_users = db.adminFilterUser("''","'ALL'", 'NULL', 'NULL')
    if request.method == 'GET':
        view_users = db.adminFilterUser(name,status, sortby, sortdir)
    else:
        # approve or decline or filter
        if request.form['submit'] == 'filter':
            name = request.form['uname']
            status = request.form['status']
            try:
                sortby = request.form['checkSort']
            except:
                sortby = ''
            try:
                sortdir = request.form['checkOrder']
            except:
                sortdir = ''
            view_users = db.adminFilterUser(name,status, sortby, sortdir)
        elif request.form['submit'] == 'approve':
            try:
                selected = request.form['radio']
                db.adminApproveUser(selected)
            except:
                print("nobody selected")
            view_users = db.adminFilterUser(name,status, sortby, sortdir)
        elif request.form['submit'] == 'decline':
            try:
                selected = request.form['radio']
                db.adminDeclineUser(selected)
            except:
                print("nobody selected")
            view_users = db.adminFilterUser(name,status, sortby, sortdir)
    return render_template('manageUser.html', users = view_users, name = name, status = status, sortBy = sortby, sortDirection = sortdir)

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
    if not loggedIn():
        return redirect(url_for('index'))
    view_history = db.customerViewHistory(session['user'])
    return render_template('viewHistory.html', history = view_history)

@app.route("/visit/history", methods=['GET', 'POST'])
def visitHistory():
    if not loggedIn():
        return redirect(url_for('index'))
    companies = db.query("select * from company;")
    companies = [company[0] for company in companies]

    start="NULL"
    end="NULL"
    
    if request.method == 'POST':
        start = request.form['start']
        end = request.form['end']

        if len(start) == 0:
            start = "NULL"
        if len(end) == 0:
            end = "NULL"
    visit_history = db.userFilterVisitHistory(session['user'], start, end)
    
    if request.method == 'POST':
        company = request.form['company']
        print(company)
        if company != 'All':
            visit_history = [visit if visit[5] == company else None for visit in visit_history]

    return render_template('visitHistory.html', companies = companies, history = visit_history)

