from flask import render_template, request, url_for, redirect
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
        return render_template('custManReg.html', messages=messages)

def register(role):
    if role == "user":
        password = request.form['password']
        confPass = request.form['confPass']
        first = request.form['first']
        last = request.form['last']
        username = request.form['username']
        if password == confPass and len(password) >= 8:
            db.userRegister(username, password, first, last)
            return redirect(url_for('index'))
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
        for i in range(0,5):
            try:
                cc = request.form['{}'.format(i)]
                print(cc)
            except:
                break
        # try:
        #     cc = request.form['0']
        #     print(cc)
        #     cc = request.form['1']
        #     print(cc)
        #     cc = request.form['2']
        #     print(cc)
        #     cc = request.form['3']
        #     print(cc)
        #     cc = request.form['4']
        #     print(cc)
        # except:
        #     print("out of bounds")
        ccs = [0000000000000000] 
        if password == confPass and len(password) >= 8 and ccs != None:
            db.userRegister(username, password, first, last)
            for cc in ccs:
                db.custAddCC(username, cc)
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
        company = requset.form['company']
        
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



