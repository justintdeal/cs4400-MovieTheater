from flask import render_template, request, url_for, redirect, session
import theater.src.procedureInterface as db


def getRegTemplate(role, messages=None):
    if role == 'user':
        return render_template('userReg.html', messages=messages)
    elif role == "manager":
        companies = [company[0] for company in db.query("select * from company")]
        return render_template('manReg.html', messages=messages, companies = companies)
    elif role == "customer":
        return render_template('custReg.html', messages=messages)
    elif role == "mancust":
        companies = [company[0] for company in db.query("select * from company")]
        return render_template('custManReg.html', messages=messages, companies = companies)

def register(role):
    if role == "user":
        password = request.form['password']
        confPass = request.form['confPass']
        first = request.form['first']
        last = request.form['last']
        username = request.form['username']
        if password == confPass and len(password) >= 8:
            try:
                db.userRegister(username, password, first, last)
            except:
                message = "User already exists!"
                return render_template("userReg.html", messages=message)
            user = db.userLogin(username, password)
            if len(user) == 0:
                message = "Invalid Login: Error registering user"
                return render_template('home.html', messages=message)
            user = user[0]
            session['active'] = True
            session['user'] = user[0]
            session['type'] = "User"
            return redirect(url_for('dashboard', user = user))
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
        ccs = []
        for i in range(0,5):
            try:
                cc = request.form['{}'.format(i)]
                ccs.append(cc)
            except:
                break
        if password == confPass and len(password) >= 8 and ccs != None:
            try:
                db.custRegister(username, password, first, last)
            except:
                message = "User already exists!"
                return render_template("custReg.html", messages=message)
            if len(ccs) == 0:
                message = "Must Have at Least One CC"
                return render_template("custReg.html", messages=message)
            for cc in ccs:
                try:
                    db.custAddCC(username, cc)
                except:
                    message = "Credit Cards Must Be Unique in System!"
                    return render_template("custReg.html", messages=message)
            user = db.userLogin(username, password)
            if len(user) == 0:
                message = "Invalid Login: Error registering user"
                return render_template('home.html', messages=message)
            user = user[0]
            session['active'] = True
            session['user'] = user[0]
            session['type'] = "Customer"
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
        company = request.form['company']
 
        if password == confPass and len(password) >= 8:
            try:
                db.manRegister(username, password, first, last, company, street, city, state, zipcode)
            except:
                message = "User already exists!"
                return render_template("manReg.html", messages=message)
            user = db.userLogin(username, password)
            if len(user) == 0:
                message = "Invalid Login: Error registering user"
                return render_template('home.html', messages=message)
            user = user[0]
            session['active'] = True
            session['user'] = user[0]
            session['type'] = "Manager"
            return redirect(url_for('dashboard', user = user))
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
        company = request.form['company']
        ccs = []
        for i in range(0,5):
            try:
                cc = request.form['{}'.format(i)]
                ccs.append(cc)
            except:
                break
        if password == confPass and len(password) >= 8 and ccs != None:
            try:
                db.manCustRegister(username, password, first, last, company, street, city, state, zipcode)
            except:
                message = "User already exists!"
                return render_template("manReg.html", messages=message)
            if len(ccs) == 0:
                message = "Must Have at Least One CC"
                return render_template("custReg.html", messages=message)
            for cc in ccs:
                try:
                    db.manCustAddCC(username, cc)
                except:
                    message = "Credit Cards Must Be Unique in System!"
                    return render_template("custReg.html", messages=message)
            user = db.userLogin(username, password)
            if len(user) == 0:
                message = "Invalid Login: Error registering user"
                return render_template('home.html', messages=message)
            user = user[0]
            session['active'] = True
            session['user'] = user[0]
            session['type'] = "ManagerCust"
            return redirect(url_for('dashboard', user = user))
        elif ccs == None:
            message = "You must add at least one credit card"
            return render_template("custManReg.html", messages=message)
        elif len(password) <= 8:
            message = "Password must be at least 8 characters"
            return render_template("custManReg.html", messages=message)
        else:
            message = "Passwords must match"
            return getRegTemplate("mancust", message)



