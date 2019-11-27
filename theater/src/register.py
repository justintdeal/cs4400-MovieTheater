from flask import render_template, request, url_for, redirect
import theater.src.procedureInterface as db


def getRegTemplate(role, messages=None):
    if role == 'user':
        return render_template('userReg.html', messages=messages)
    elif role == "manager":
        return render_template('manReg.html', messages=messages)
    elif role == "customer":
        return render_template('custReg.html', messages=messages)
    elif role == "mancust":
        return render_template('custManReg.html', messages=messages)

def register(role):
    if role == "user":
        password = request.form['password']
        confPass = request.form['confPass']
        first = request.form['first']
        last = request.form['last']
        username = request.form['username']
    
        # print(password)
        # print(confPass)
        # print(first)
        # print(last)
        # print(username)
        if password == confPass and len(password) >= 8:
            db.userRegister(username, password, first, last)
            # user = db.userLogin(username, password)
            # print(user)
            # if len(user) == 0:
            #     message = "Invalid Login"
            #     return redirect(url_for('index'))
            # return redirect(url_for('dashboard', user = user))
            return render_template('home.html')
        elif len(password) <= 8:
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
            
        #need to fix but temp credit card
        ccs = [0000000000000000] 
        if password == confPass and len(password) >= 8 and ccs != None:
            db.userRegister(username, password, first, last)
            for cc in ccs:
                db.custAddCC(user, cc)
            user = db.userLogin(user, password)
            return redirect(url_for('dashboard', user = user))
        elif ccs == None:
            message = "You must add at least one credit card"
            return render_template("custReg.html", messages=message)
        elif len(password) <= 8:
            message = "Password must be at least 8 characters"
            return render_template("custReg.html", messages=message)
        else:
            message = "Passwords must match"
            return getRegTemplate("customer", message)
        
    if role == "manager":
        password = request.form['password']
        confPass = request.form['confPass']
        first = request.form['first']
        last = request.form['last']
        username = request.form['username']
        street = request.form['street']
        city = request.form['city']
        state = request.form['state']
        zipcode = request.form['zipcode']
        #get correct company
        company = "amc"
 
        if password == confPass and len(password) >= 8:
            db.manRegister(username, password, first, last, company, street, city, state, zipcode)
            user = db.userLogin(user, password)
            redirect(url_for('dashboard', user = user))
        elif len(password) <= 8:
            message = "Password must be at least 8 characters"
            return render_template("manReg.html", messages=message)
        else:
            message = "Passwords must match"
            return getRegTemplate("manager", message)
        
    if role == "mancust":
        password = request.form['password']
        confPass = request.form['confPass']
        first = request.form['first']
        last = request.form['last']
        username = request.form['username']
        street = request.form['street']
        city = request.form['city']
        state = request.form['state']
        zipcode = request.form['zipcode']
        #get correct company
        company = "amc"
        ccs = [0000000000000000]
        if password == confPass and len(password) >= 8 and ccs != None:
            db.manCustRegister(username, password, first, last, company, street, 
            city, state, zipcode)
            for cc in ccs:
                manCustAddCC(user, cc)
            redirect(url_for('dashboard', user = user))
        elif ccs == None:
            message = "You must add at least one credit card"
            return render_template("custManReg.html", messages=message)
        elif len(password) <= 8:
            message = "Password must be at least 8 characters"
            return render_template("custManReg.html", messages=message)
        else:
            message = "Passwords must match"
            return getRegTemplate("mancust", message)



