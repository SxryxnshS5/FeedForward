from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
