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
#finished
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
#finished
@app.route("/register")
def registerHome():
    return render_template('registerHome.html')

#screens 3-6
#user works
#customer procedure is broken / need to figure out cc issue
#manager 
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
                sortdirnum = request.form['checkOrder']
                if (sortdirnum == '1' and (sortby == 'username' or sortby == '')):
                    sortdir = 'ASC'
                elif (sortdirnum == '2' and sortby == 'creditCardCount'):
                    sortdir = 'ASC'
                elif (sortdirnum == '3' and sortby == 'userType'):
                    sortdir = 'ASC'
                elif (sortdirnum == '4' and sortby == 'status'):
                    sortdir = 'ASC'
                else:
                    sortdir = ''
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
    return render_template('manageUser.html', users = view_users)

#screen 14
@app.route("/manage/company", methods=['GET', 'POST'])
def manageCompany():
    if not loggedIn():
        return redirect(url_for('index'))
    name = 'ALL'
    minCity = 'NULL'
    maxCity = 'NULL'
    minTh = 'NULL'
    maxTh = 'NULL'
    minEmp = 'NULL'
    maxEmp = 'NULL'
    sortby = ''
    sortdir = ''
    if request.method == 'GET':
        view_comps = db.adminFilterCompany(name,minCity,maxCity,minTh,maxTh,minEmp,maxEmp,sortby,sortdir)
    else:
        if request.form['submit'] == 'filter':
            name = request.form['company']
            if len(request.form['lowCity']) != 0:
                minCity = "'{}'".format(request.form['lowCity'])
            if len(request.form['upCity']) != 0:
                maxCity = "'{}'".format(request.form['upCity'])
            if len(request.form['lowTheater']) != 0:
                minTh = "'{}'".format(request.form['lowTheater'])
            if len(request.form['upTheater']) != 0:
                maxTh = "'{}'".format(request.form['upTheater'])
            if len(request.form['lowEmp']) != 0:
                minEmp = "'{}'".format(request.form['lowEmp'])
            if len(request.form['upEmp']) != 0:
                maxEmp = "'{}'".format(request.form['upEmp'])
            try:
                sortby = request.form['checkSort']
            except:
                sortby = ''
            try:
                sortdirnum = request.form['checkOrder']
                if (sortdirnum == '1' and (sortby == 'comName' or sortby == '')):
                    sortdir = 'ASC'
                elif (sortdirnum == '2' and sortby == 'numCityCover'):
                    sortdir = 'ASC'
                elif (sortdirnum == '3' and sortby == 'numTheater'):
                    sortdir = 'ASC'
                elif (sortdirnum == '4' and sortby == 'numEmployee'):
                    sortdir = 'ASC'
                else:
                    sortdir = ''
            except:
                sortdir = ''
            view_comps = db.adminFilterCompany(name,minCity,maxCity,minTh,maxTh,minEmp,maxEmp,sortby,sortdir)
        elif request.form['submit'] == 'create':
            return redirect(url_for('createTheater'))
        elif request.form['submit'] == 'detail':
            try:
                selected = request.form['radio']
                return redirect(url_for('viewCompany', name = selected))
            except:
                print("none selected")

        #view_comps = db.adminFilterCompany(name,minCity,maxCity,minTh,maxTh,minEmp,maxEmp,sortby,sortdir)
    return render_template('manageCompany.html', comps = view_comps)

#screen 15: Admin Create Theater
@app.route("/manage/company/create/theater", methods=['GET', 'POST'])
def createTheater():
    companies = db.query("select * from company;")
    companies = [company[0] for company in companies]

    managers = db.query("select username, company from manager;")
    managers = [man[0] + " (" + man[1] + ")" for man in managers]


    if request.method == "POST":
        name = request.form['name']
        company = request.form['company']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zipcode = request.form['zipcode']
        cap = request.form['cap']
        manager  = request.form['manager']
        
        if manager == "Choose..." or company == "Choose...":
            "sad"
        else:
            space = " " 

            manager = manager[0:manager.index(space)]
            db.adminCreateTheater(name, company, address, city, state, zipcode, cap, manager)


    # managers = db.query("select * from ")
    return render_template('createTheater.html', companies = companies, managers = managers)

#screen 16: Admin Company Detail
@app.route("/manage/company/<name>", methods=['GET', 'POST'])
def viewCompany(name):
    if not loggedIn():
        return redirect(url_for('index'))
    name = name.split('_')
    name = ' '.join(name)
    
    employee = db.adminViewComDetail_emp(name)
    theaters = db.adminViewComDetail_th(name)

    employees = [name[0] + " " + name[1] for name in employee]

    return render_template('viewCompany.html', employees = employees, theaters = theaters, name = name)

#screen 17: Admin Create Movie
#finished
@app.route("/manage/company/createMovie/", methods=['GET', 'POST'])
def createMovie():
    if not loggedIn():
        return redirect(url_for('index'))
    
    message = None

    if request.method == "POST":
        movie = request.form['movie']
        duration = request.form['dur']
        rd = request.form['rd']

        if len(movie)== 0:
            message = "Please Name The Movie"
        if len(duration) == 0:
            message = "Please Choose a Duration (Minutes)"
        if len(rd) == 0:
            message = "Please Enter a Release Date"
        else:
            db.adminCreateMovie(movie, duration, rd)
            message = "Movie Created"

    return render_template('createMovie.html', messages=message)

#Screen 18: Manager Theater Overview 
#finished
@app.route("/theater/overview", methods=['GET', 'POST'])
def theaterOverview():
    if not loggedIn():
        return redirect(url_for('index'))
    
    movie=''
    durStart='NULL'
    durEnd='NULL'
    minRd = 'NULL'
    maxRd = 'NULL'
    minPd = 'NULL'
    maxPd = 'NULL'
    np = False

    if request.method == "POST":
        movie = request.form['movie']
        durStart = request.form['durStart']
        durEnd = request.form['durEnd']
        minRd = request.form['minRd']
        maxRd = request.form['maxRd']
        minPd = request.form['minPd']
        maxPd = request.form['maxPd']
        np = 'np' in request.form

        if len(movie) == 0:
            movie = ''
        if len(durStart) == 0:
            durStart = 'NULL'
        if len(durEnd) == 0:
            durEnd = 'NULL'
        if len(minRd) == 0:
            minRd = 'NULL'
        if len(maxRd) == 0:
            maxRd = 'NULL'
        if len(minPd) == 0:
            minPd = 'NULL'
        if len(maxPd) == 0:
            maxPd = 'NULL'

    data = db.manageFilterTheater(session['user'], movie, durStart, durEnd, minRd, maxRd, minPd, maxPd, np)


    return render_template('theaterOverview.html', datas =data)


#screen 19: Manager Schedule Movie 
#fixed except maybe ''s
@app.route("/manage/company/schedule/movie", methods=['GET', 'POST'])
def scheduleMovie():
    if not loggedIn():
        return redirect(url_for('index'))
    movies = db.query("select * from movie;")
    movies = [movie[0] for movie in movies]
    message = None

    if request.method == 'POST':
        rd = request.form['rd']
        pd = request.form['pd']
        movie = request.form['movie']

        if len(rd) == 0:
            message = "You Must Select a Release Date"
        elif len(pd) == 0:
            message = "You Must Select a Play Date"
        else:
            message = db.managerScheduleMovie(session['user'], movie, rd, pd)

    return render_template('scheduleMovie.html', movies = movies, messages = message)

#Screen 20: Customer Explore Movie
#finished
@app.route("/movie/explore", methods=['GET', 'POST'])
def exploreMovie():
    if not loggedIn():
        return redirect(url_for('index'))
    
    companies = db.query("select * from company;")
    companies = [company[0] for company in companies]

    movies = db.query("select * from movie;")
    movies = [movie[0] for movie in movies]
    
    user = session['user']
    sql = "select creditCardNum from creditCard where username = '" + user + "';"
    ccs = db.query(sql)
    ccs = [cc[0] for cc in ccs]

    movie = "All"
    company = ""
    city = ""
    state = ""
    pd_start = 'NULL'
    pd_end = 'NULL'

    if request.method == "POST":
        if request.form['hidden'] == 'true':
            movie = request.form['movie']
            company = request.form['company']
            if company == "All":
                company = ''
            city = request.form['city']
            if len(city) == 0:
                city = ''
            state = request.form['state']
            if state == 'All':
                state = ''
            pd_start = request.form['pd_start']
            if len(pd_start) == 0:
                pd_start = 'NULL'
            pd_end = request.form['pd_end']
            if len(pd_end) == 0:
                pd_end = 'NULL'
        else:
            cc = request.form['cc']
            data = request.form['th_group'].split('|')
            mv = data[0]
            rd = data[1]
            th = data[2]
            com = data[3]
            pd = data[4]
            db.customerViewMovie(cc, mv, rd, th, com, pd)

    filtered = db.customerFilterMovie(movie, company, city, state, pd_start, pd_end)
    return render_template('exploreMovie.html', datas = filtered, companies = companies, movies= movies, ccs=ccs)

#Screen 21: Customer View History 
#Finished
@app.route("/movie/history", methods=['GET', 'POST'])
def viewHistory():
    if not loggedIn():
        return redirect(url_for('index'))
    view_history = db.customerViewHistory(session['user'])
    return render_template('viewHistory.html', history = view_history)

#Screen 22: User Explore Theater
#finished but need to fix ''s
@app.route("/theater/explore", methods=['GET', 'POST'])
def exploreTheater():
    if not loggedIn():
        return redirect(url_for('index'))
    
    theaters_full = db.query("select * from theater;")
    theaters = set([theater[1] for theater in theaters_full])
    data = theaters_full

    companies = db.query("select * from company;")
    companies = [company[0] for company in companies]


    message = None
    if request.method == 'POST':
        if request.form['hidden'] == "hidden":
            theater = request.form['theater']
            if len(theater) == 0:
                theater = ""
            company = request.form['company']
            if len(company) == 0:
                company = ""
            city = request.form['city']
            if len(city) == 0:
                city = ""
            state = request.form['state']
            if len(state) == 0:
                state = ""
            data = db.userFilterTheater(theater, company, city, state)
        else:
            theater_group = request.form['th']
            if len(theater_group) == 0:
                message = "You must select a theater"
            visit_date = request.form['vd']
            if len(visit_date) == 0:
                message = "You Must Select A Visit Date"
            else: 
                ind = None
                for i in range(len(theater_group)):
                    if theater_group[i] == '|':
                        ind = i
                th = theater_group[0:ind]
                comp  = theater_group[ind+1:]

                db.userVisitTheater(th, comp, visit_date, session['user'])
                message = "Added"

    return render_template('exploreTheater.html', messages = message, datas = data, theaters = theaters, companies = companies)

#screen 23: User Visit History
#finished
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

