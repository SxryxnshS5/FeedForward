import os
from flask import Flask, render_template
from dotenv import load_dotenv
from extensions import init_app, db, login_manager, csrf


app = Flask(__name__)

# Configuring the secret key to sign and validate session cookies.
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Initialize extensions
init_app(app)


@login_manager.user_loader
def load_user(id):
    from models import User
    """ user loader function for LoginManager to get user instances from the db """
    return User.query.get(int(id))


# Define your Flask routes to render the HTML templates
@app.route('/')
def index():
    return render_template('main/index.html')


@app.route('/about')
def about():
    return render_template('main/about.html')


@app.route('/newsletter')
def newsletter():
    return render_template('main/newsletter.html')

@app.route('/create_admin_account')
def create_admin_account():
    return render_template('main/create_admin_account.html')


# Errors
@app.errorhandler(400)
def bad_request(error):
    return render_template('errors/400.html'), 400

@app.errorhandler(403)
def forbidden(error):
    return render_template('errors/403.html'), 403

@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

@app.errorhandler(503)
def service_unavailable(error):
    return render_template('errors/503.html'), 503


if __name__ == '__main__':
    # Import blueprints (imported here to avoid Circular Import Error)
    from users.views import users_blueprint
    from admin.views import admin_blueprint
    from adverts.views import adverts_blueprint
    from messages.views import messages_blueprint

    # Register blueprints with app
    app.register_blueprint(users_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(adverts_blueprint)
    app.register_blueprint(messages_blueprint)
    app.run(debug=True)
