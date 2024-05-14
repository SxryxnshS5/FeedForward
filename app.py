import os
from flask import Flask, render_template
from dotenv import load_dotenv

app = Flask(__name__)

# Configuring the secret key to sign and validate session cookies.
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET KEY')

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

if __name__ == '__main__':
    app.run(debug=True)