from flask import Flask, render_template, request

app = Flask(__name__)

#This is where the user will login
#if get show login form if post show validate login
#users can also go to register pages from here
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        return "hello"

@app.route("/register")
def regiserHome():
    return render_template('registerHome.html')



