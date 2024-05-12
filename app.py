from flask import Flask, render_template

app = Flask(__name__)

# Define your Flask route to render the HTML template
@app.route('/')
def index():
    return render_template('main/index.html')

if __name__ == '__main__':
    app.run(debug=True)
