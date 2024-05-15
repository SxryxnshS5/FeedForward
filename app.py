import os
from flask import Flask, render_template
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

# Configuring the secret key to sign and validate session cookies.
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET KEY')

# setup database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_ECHO'] = os.getenv('SQLALCHEMY_ECHO') == 'True'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS') == 'True'
db = SQLAlchemy(app)

# initialise instance of LoginManager
login_manager = LoginManager()
# set view function which renders login page
login_manager.login_view = 'users.login'
# register LoginManager instance with app
login_manager.init_app(app)

from models import User
@login_manager.user_loader
def load_user(email):
    """ user loader function for LoginManager to get user instances from the db """
    return User.query.filter_by(email=email).first()

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

@app.route('/adminaccount')
def adminaccount():
    return render_template('main/adminaccount.html')

@app.route('/newsletter')
def newsletter():
    return render_template('main/newsletter.html')

@app.route('/create_admin_account')
def create_admin_account():
    return render_template('main/create_admin_account.html')

# Import blueprints (imported here to avoid Circular Import Error)
from users.views import users_blueprint

# Register blueprints with app
app.register_blueprint(users_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
