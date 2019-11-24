from theater import app
import mysql.connector

#db connection info
user = None
password = None
host = None

def connect():
    connection = mysql.connector.connect(user=user, password=password,
                                        host=host)
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
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data


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
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data

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
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data

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