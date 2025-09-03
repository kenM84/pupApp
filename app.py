import os
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for, flash)
from flask_session import Session
from flask_login import (LoginManager, login_required, login_user,
                         logout_user)
from .services.auth_service import AuthService




app = Flask(__name__)

# Configure session management
app.config['SECRET_KEY'] = os.environ.get(
    'SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'pupapp:'
app.config['SESSION_FILE_DIR'] = './flask_session'

# Initialize session
Session(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# Initialize auth service
auth_service = AuthService()

@login_manager.user_loader
def load_user(user_id):
    return auth_service.get_user_by_id(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        next_page = request.args.get('next')

        if not username or not password:
            flash('Please enter both username and password.', 'error')
            return render_template('login.html')

        user, message = auth_service.authenticate_user(username, password)

        if user:
            login_user(user, remember=True)
            flash('Login successful!', 'success')
            return redirect(next_page or url_for('index'))
        else:
            flash(message, 'error')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not all([username, email, password, confirm_password]):
            flash('Please fill in all fields.', 'error')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('register.html')

        user, message = auth_service.create_user(username, email, password)

        if user:
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash(message, 'error')

    return render_template('register.html')


@app.route('/greyscale_demo')
@login_required
def greyscale_demo():
    return render_template('greyscale_index.html')


@app.route('/')
@login_required
def index():
    print('Request for index page received')
    # key_agent = KeyVaultService()

    # Run async methods in a new event loop
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # try:
    #     loop.run_until_complete(key_agent.configure())
    #     dbserver = loop.run_until_complete(
    #         key_agent.get_secret("sqlDBServer"))
    # finally:
    #     loop.close()
    #
    return render_template('greyscale_index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/hello', methods=['POST'])
def hello():
    name = request.form.get('name')

    if name:
        print('Request for hello page received with name=%s' % name)
        return render_template('hello.html', name=name)
    else:
        print('Request for hello page received with no name or blank name '
              '-- redirecting')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
