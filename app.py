import os
from flask import Flask, render_template
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

csrf = CSRFProtect(app)

# Configuring the secret key to sign and validate session cookies.
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

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


@login_manager.user_loader
def load_user(email):
    from models import User
    """ user loader function for LoginManager to get user instances from the db """
    return User.query.filter_by(email=email).first()


# Define your Flask route to render the HTML template
@app.route('/')
def index():
    return render_template('main/index.html')




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


@app.route('/create_advert')
def create_advert():
    return render_template('main/createadvert.html')


if __name__ == '__main__':
    # Import blueprints (imported here to avoid Circular Import Error)
    from users.views import users_blueprint
    from admin.views import admin_blueprint

    # Register blueprints with app
    app.register_blueprint(users_blueprint)
    app.register_blueprint(admin_blueprint)
    app.run(debug=True)
