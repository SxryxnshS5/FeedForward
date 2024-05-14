import os
from flask import Flask, render_template
from dotenv import load_dotenv

app = Flask(__name__)

# Configuring the secret key to sign and validate session cookies
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET KEY')

# Define your Flask route to render the HTML template
@app.route('/')
def index():
    return render_template('main/index.html')


if __name__ == '__main__':
    app.run(debug=True)
