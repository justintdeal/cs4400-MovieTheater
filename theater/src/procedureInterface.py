from theater import app
import mysql.connector

#db connection info
user = "team50"
password = "Columns1!"
host = "127.0.0.1"
db = 'team50'

def connect():
    connection = mysql.connector.connect(user=user, password=password, host=host, db=db)
    return connection

def query(sql):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data

### Executes Stored Percedures
#screen 1
def userLogin(user, password):
    connection = connect()
    cursor = connection.cursor()
    sql = "use `team50`;"
    cursor.execute(sql)
    sql = "call user_login('{}', '{}');".format(user, password)
    cursor.execute(sql)
    sql = "select * from UserLogin;"
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data

#screen 3
def userRegister(user, password, first, last):
    connection = connect()
    cursor = connection.cursor()
    sql = "call user_register('{}','{}','{}','{}');".format(user, password, first, last)
    cursor.execute(sql)
    cursor.close()
    connection.close()

#screen 4
def custRegister(user, password, first, last):
    connection = connect()
    cursor = connection.cursor()
    sql = "call customer_only_register(@{}, @{}, @{}, \
           @{});".format(user, password, first, last)
    cursor.execute(sql)
    cursor.close()
    connection.close()

#screen 4
def custAddCC(user, cc):
    connection = connect()
    cursor = connection.cursor()
    sql = "call customer_add_creditcard(@{}, \
           @{});".format(user, cc)
    cursor.execute(sql)
    cursor.close()
    connection.close()

#screen 5
def manRegister(user, password, first, last, company, street, 
                city, state, zipcode):
    connection = connect()
    cursor = connection.cursor()
    sql = "call manager_only_register(@{}, @{}, @{}, @{},\
           @{},@{}, @{}, @{}, @{});".format(user, password, first, last, 
           company, street, city, state, zipcode)
    cursor.execute(sql)
    cursor.close()
    connection.close()

#screen 6
def manCustRegister(user, password, first, last, company, street, 
                city, state, zipcode):
    connection = connect()
    cursor = connection.cursor()
    sql = "call manager_customer_register(@{}, @{}, @{}, @{}, @{},\
           @{}, @{}, @{}, @{});".format(user, password, first, last, 
           company, street, city, state, zipcode)
    cursor.execute(sql)
    cursor.close()
    connection.close()

#screen 6
def manCustAddCC(user, cc):
    connection = connect()
    cursor = connection.cursor()
    sql = "call manager_customer_add_creditcard(@{}, @{});".format(user, cc)
    cursor.execute(sql)
    cursor.close()
    connection.close()

#screen 13
def adminApproveUser(user):
    connection = connect()
    cursor = connection.cursor()
    sql = "call admin_approve_user(@{});".format(user)
    cursor.execute(sql)
    cursor.close()
    connection.close()

#screen 13
def adminDeclineUser(user):
    connection = connect()
    cursor = connection.cursor()
    sql = "call admin_decline_user(@{});".format(user)
    cursor.execute(sql)
    cursor.close()
    connection.close()

#screen 13
def adminFilterUser(user, status, sortBy, sortDirection):
    connection = connect()
    cursor = connection.cursor()
    sql = "EXEC admin_filter_user(@{}, @{}\
           @{}, @{});".format(user, status, 
           sortBy, sortDirection)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data
    
#screen 14    
def adminFilterCompany(comName, minCity, maxCity, minTheater,  
            maxTheater, minEmp, maxEmp, sortBy, sortDirection):
    connection = connect()
    cursor = connection.cursor()
    sql = "call admin_filter_company(@{}, @{}\
           @{}, @{}, @{}, \
           @{} , @{}, @{} @{});".format(comName, minCity, maxCity, 
           minTheater, maxTheater, minEmp, maxEmp, sortBy, sortDirection)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data

#screen 15
def adminCreateTheater(theaterName, comName, street, city, state, 
                        zipcode, cap, manUser):
    connection = connect()
    cursor = connection.cursor()
    sql = "call admin_create_theater(@{}, @{},\
           @{}, @{}, @{}, \
           @{}, @{}, @{});".format(theaterName, comName, street, city, state, 
           zipcode, cap, manUser)
    cursor.execute(sql)
    cursor.close()
    connection.close()

#screen 16                
def adminViewComDetail_emp(company):
    connection = connect()
    cursor - connection.cursor()
    sql = "call admin_view_comDetail_emp(@{});".format(company)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data

#screen 16
def adminViewComDetail_th(company):
    connection = connect()
    cursor - connection.cursor()
    sql = "call admin_view_comDetail_th(@{});".format(company)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data

#screen 17
def adminCreateMovie(movie, duration, releaseDate):
    connection = connect()
    cursor = connection.cursor()
    sql = "call admin_create_mov(@{}, @{}, \
           @{});".format(movie, duration, releaseDate)
    cursor.execute(sql)
    cursor.close()
    connection.close()

#screen 18
def manageFilterTheater(manUser, movie, minDur, maxDur, minMovRD, 
             maxMovRD, minMovPD, maxMovPD, includeNotPlayed):
    connection = connect()
    cursor = connection.cursor()
    sql = "call manager_filter_th(@{}, @{}, @{}, @{}, \
           @i{}, @{}, @{});".format(manUser, movie, minDur, maxDur, minMovRD, maxMovRD, minMovPD,
           maxMovPD, includeNotPlayed)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data 

#screen 19
def managerScheduleMovie(manUser, movie, movRD, movPD):
    connection = connect()
    cursor = connection.cursor()
    sql = "call manage_schedule_mov(@{}, @{}, \
           @{}, @{});".format(manUser, movie, movRD, movPD)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data

#screen 20
def customerFilterMovie(movName, comName, city, state, 
            minMovPlayDate, maxMovPlayDate):
    connection = connect()
    cursor = connection.cursor()
    sql = "call customer_filter_mov(@{}, @{},\
           @{}, @{}, @{}, @{});".format(movName, comName, city, state, 
            minMovPlayDate, maxMovPlayDate)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data

#screen 20
def customerViewMovie(i_creditCardNum, i_movName, i_movReleaseDate, i_thName, 
                i_comName, i_movPlayDate):
    connection = connect()
    cursor - connection.cursor()
    sql = "call customer_view_mov(@{}, @{}, @{} \
           @{}, @{}, @{});".format(i_creditCardNum, 
           i_movName, i_movReleaseDate, i_thName, i_comName, i_movPlayDate)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    connection.close()

#screen 21
def customerViewHistory(user):
    connection = connect()
    cursor - connection.cursor()
    sql = "call customer_view_history(@{});".format(user)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data

#screen 22
def userFilterTheater(i_thName, i_comName, i_city, i_state):
    connection = connect()
    cursor - connection.cursor()
    sql = "call user_filter_th(@{}, @{}, @{},\
           @{});".format(i_thName, i_comName, i_city, i_state)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data

#screen 22
def userVisitTheater(i_thName, i_comName, i_visitDate, i_username):
    connection = connect()
    cursor - connection.cursor()
    sql = "call user_visit_th(@{},@{},@{},@{});".format(i_thName, i_comName, i_visitDate, i_username)
    cursor.execute(sql)
    cursor.close()
    connection.close()

#screen 23
def userFilterVisitHistory(i_username, i_minVisitDate, i_maxVisitDate):
    connection = connect()
    cursor - connection.cursor()
    sql = "call user_filter_visitHistory(@{}, @{},\
           @{};".format(i_username, i_minVisitDate, i_maxVisitDate)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data