from theater import app
import mysql.connector

#db connection info
user = "team50"
password = "Columns1!"
host = "127.0.0.1"

def connect():
    connection = mysql.connector.connect(user=user, password=password, host=host)
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
def userLogin(user, password):
    connection = connect()
    cursor = connection.cursor()
    sql = "EXEC user_login @i_username = {}, @i_password = {}".format(user, password)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data

def userRegister(user, password, first, last):
    connection = connect()
    cursor = connection.cursor()
    sql = "EXEC user_register @i_username = {}, \
           @i_password = {}, @i_firstname = {}, \
           @i_lastname = {}".format(user, password, first, last)
    cursor.execute(sql)
    cursor.close()
    connection.close()

def custRegister(user, password, first, last):
    connection = connect()
    cursor = connection.cursor()
    sql = "EXEC customer_only_register @i_username = {}, \
           @i_password = {}, @i_firstname = {}, \
           @i_lastname = {}".format(user, password, first, last)
    cursor.execute(sql)
    cursor.close()
    connection.close()

def custAddCC(user, cc):
    connection = connect()
    cursor = connection.cursor()
    sql = "EXEC customer_add_creditcard @i_username \
           = {}, @i_creditCardNum = {}".format(user, cc)
    cursor.execute(sql)
    cursor.close()
    connection.close()


def manRegister(user, password, first, last, company, street, 
                city, state, zipcode):
    connection = connect()
    cursor = connection.cursor()
    sql = "EXEC manager_only_register @i_username = {}, @i_password \
           = {}, @i_firstname = {}, @i_lastname = {}, @i_comName = {},\
           @i_empStreet = {}, @i_empCity = {}, @i_empState = {}, \
           @i_empZipcode = {}".format(user, password, first, last, 
           company, street, city, state, zipcode)
    cursor.execute(sql)
    cursor.close()
    connection.close()

def manCustRegister(user, password, first, last, company, street, 
                city, state, zipcode):
    connection = connect()
    cursor = connection.cursor()
    sql = "EXEC manager_customer_register @i_username = {}, @i_password \
           = {}, @i_firstname = {}, @i_lastname = {}, @i_comName = {},\
           @i_empStreet = {}, @i_empCity = {}, @i_empState = {}, \
           @i_empZipcode = {}".format(user, password, first, last, 
           company, street, city, state, zipcode)
    cursor.execute(sql)
    cursor.close()
    connection.close()

def manCustAddCC(user, cc):
    connection = connect()
    cursor = connection.cursor()
    sql = "EXEC manager_customer_add_creditcard @i_username \
           = {}, @i_creditCardNum = {}".format(user, cc)
    cursor.execute(sql)
    cursor.close()
    connection.close()

def adminApproveUser(user):
    connection = connect()
    cursor = connection.cursor()
    sql = "EXEC admin_approve_user @i_username = {}".format(user)
    cursor.execute(sql)
    cursor.close()
    connection.close()

def adminDeclineUser(user):
    connection = connect()
    cursor = connection.cursor()
    sql = "EXEC admin_decline_user @i_username = {}".format(user)
    cursor.execute(sql)
    cursor.close()
    connection.close()

def adminFilterUser(user, status, sortBy, sortDirection):
    connection = connect()
    cursor = connection.cursor()
    sql = "EXEC admin_filter_user @i_username = {}, @i_status = {}\
           @i_sortBy = {}, @i_sortDirection = {}".format(user, status, 
           sortBy, sortDirection)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data
    
def adminFilterCompany(comName, minCity, maxCity, minTheater,  
            maxTheater, minEmp, maxEmp, sortBy, sortDirection):
    connection = connect()
    cursor = connection.cursor()
    sql = "EXEC admin_filter_company @i_comName = {}, @i_minCity = {}\
           @i_maxCity = {}, @i_minTheater = {}, @i_maxTheater = {}, \
           @i_minEmployee = {} , @i_maxEmployee = {}, @i_sortBy = {} \
           @i_sortDirection = {}".format(comName, minCity, maxCity, 
           minTheater, maxTheater, minEmp, maxEmp, sortBy, sortDirection)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data

def adminCreateTheater(theaterName, comName, street, city, state, 
                        zipcode, cap, manUser):
    connection = connect()
    cursor = connection.cursor()
    sql = "EXEC admin_create_theater @i_thName = {}, @i_comName = {},\
           @i_thStreet = {}, @i_thCity = {}, @i_thState = {}, \
           @i_thZipcode = {}, @i_capacity = {}, @i_managerUsername \
           = {}".format(theaterName, comName, street, city, state, 
           zipcode, cap, manUser)
    cursor.execute(sql)
    cursor.close()
    connection.close()

                
def adminViewComDetail_emp(company):
    connection = connect()
    cursor - connection.cursor()
    sql = "EXEC admin_view_comDetail_emp @i_comName = {}".format(company)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data

def adminViewComDetail_th(company):
    connection = connect()
    cursor - connection.cursor()
    sql = "EXEC admin_view_comDetail_th @i_comName = {}".format(company)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data

def adminCreateMovie(movie, duration, releaseDate):
    connection = connect()
    cursor = connection.cursor()
    sql = "EXEC admin_create_mov @i_movName= {}, @i_movDuration = \
           {}, @i_movReleaseDate".format(movie, duration, releaseDate)
    cursor.execute(sql)
    cursor.close()
    connection.close()

def manageFilterTheater(manUser, movie, minDur, maxDur, minMovRD, 
             maxMovRD, minMovPD, maxMovPD, includeNotPlayed):
    connection = connect()
    cursor = connection.cursor()
    sql = "EXEC manager_filter_th @i_manUsername = {}, @i_movName = \
           {}, @i_minMovDuration = {}, @i_maxMovDuration = {}, \
           @i_minMovPlayDate = {}, @i_maxMovPlayDate = {}, i_includeNotPlayed\
           ={}".format(manUser, movie, minDur, maxDur, minMovRD, maxMovRD, minMovPD,
           maxMovPD, includeNotPlayed)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data 

def managerScheduleMovie(manUser, movie, movRD, movPD):
    connection = connect()
    cursor = connection.cursor()
    sql = "EXEC manage_schedule_mov @i_manUsername = {}, @i_movName = {}, \
           @i_movReleaseDate = {}, i_movPlayDate = {}".format(manUser, movie, 
           movRD, movPD)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data

def customerFilterMovie(movName, comName, city, state, 
            minMovPlayDate, maxMovPlayDate):
    connection = connect()
    cursor = connection.cursor()
    sql = "EXEC customer_filter_mov @i_movName = {}, @i_comName={},\
           @i_city = {}, @i_state = {}, minMovPlayDate = {}, \
           @i_maxMovPlayDate={}".format(movName, comName, city, state, 
            minMovPlayDate, maxMovPlayDate)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data


def customerViewMovie(i_creditCardNum, i_movName, i_movReleaseDate, i_thName, 
                i_comName, i_movPlayDate):
    connection = connect()
    cursor - connection.cursor()
    sql = "EXEC customer_view_mov @i_creditCardNum = {}, i_movName = {}, i_movReleaseDate \
           = {}, i_thName = {}, @i_comName = {}, i_movPlayDate = {}".format(i_creditCardNum, 
           i_movName, i_movReleaseDate, i_thName, i_comName, i_movPlayDate)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    connection.close()

def customerViewHistory(user):
    connection = connect()
    cursor - connection.cursor()
    sql = "EXEC customer_view_history @i_cusUsername = {}".format(user)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data

def userFilterTheater(i_thName, i_comName, i_city, i_state):
    connection = connect()
    cursor - connection.cursor()
    sql = "EXEC user_filter_th @i_thName = {}, @i_comName = {}, @i_city = {},\
           @i_state = {}".format(i_thName, i_comName, i_city, i_state)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data

def userVisitTheater(i_thName, i_comName, i_visitDate, i_username):
    connection = connect()
    cursor - connection.cursor()
    sql = "EXEC user_visit_th i_thName = {}, i_comName = {}, i_visitDate = {}, \
           i_username={}".format(i_thName, i_comName, i_visitDate, i_username)
    cursor.execute(sql)
    cursor.close()
    connection.close()

def userFilterVisitHistory(i_username, i_minVisitDate, i_maxVisitDate):
    connection = connect()
    cursor - connection.cursor()
    sql = "EXEC user_filter_visitHistory @i_username = {}, @i_minVisitDate = {},\
           i_maxVisitDate = {}".format(user)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data