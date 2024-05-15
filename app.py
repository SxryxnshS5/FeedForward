import os
from flask import Flask, render_template
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuring the secret key to sign and validate session cookies.
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET KEY')

# setup database
#TODO move to .env
app.config['SQLALCHEMY_DATABASE_URI'] = \
    "mysql+mysqlconnector://root:password@localhost:3306/2033foodsharing"
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Define your Flask route to render the HTML template
@app.route('/')
def index():
    return render_template('main/index.html')


@app.route('/login')
def login():
    return render_template('main/login.html')


@app.route('/signup')
def signup():
    return render_template('main/signup.html')

@app.route('/account')
def account():
    return render_template('main/account.html')

@app.route('/about')
def about():
    return render_template('main/about.html')

@app.route('/newsletter')
def newsletter():
    return render_template('main/newsletter.html')

@app.route('/create_admin_account')
def create_admin_account():
    return render_template('main/create_admin_account.html')

if __name__ == '__main__':
    app.run(debug=True)
