# import libraries and other files
import os
from random import randint

import werkzeug.exceptions
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mail import Mail, Message
import user_handler as uh
import credential_validate as cv
from datetime import datetime, timedelta

# define app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'lucid.log.confirmations@gmail.com'
app.config['MAIL_PASSWORD'] = 'xtqq jbky pnip cyud'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

email_timeout_duration = 60 * 2


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.route('/')
def home():
    session.pop('password_reset_user', None)
    return render_template('home.html', logged_in=logged_in())


@app.route('/login')
def login():
    session.pop('password_reset_user', None)
    if logged_in():
        return redirect(url_for('home'))
    return render_template('login.html', logged_in=logged_in())


@app.route('/login-redirect', methods=['GET', 'POST'])
def login_redirect():
    session.pop('password_reset_user', None)
    try:
        if uh.validate_login(request.form['email'], request.form['password']):
            session["logged_in"] = True
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Incorrect username / password", logged_in=logged_in())
    except werkzeug.exceptions.BadRequest as er:
        return redirect(url_for("login"))


@app.route('/signup')
def signup():
    session.pop('password_reset_user', None)
    if logged_in():
        return redirect(url_for('home'))
    return render_template('signup.html', logged_in=logged_in())


@app.route('/signup-redirect', methods=['GET', 'POST'])
def signup_redirect():
    session.pop('password_reset_user', None)
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        dob_day = request.form['dob_day']
        dob_month = request.form['dob_month']
        dob_year = request.form['dob_year']
        validation = cv.credential_validation(username, email,
                                              password, confirm_password,
                                              dob_year, dob_month, dob_day)

        if len(validation) > 0:
            return render_template('signup.html', error=validation, logged_in=logged_in())
        else:
            return render_template('login.html', error=validation, logged_in=logged_in())
    return redirect(url_for("login"))


@app.route('/submit-email', methods=['GET', 'POST'])
def submit_email():
    session.pop('password_reset_user', None)
    if request.method == 'POST':
        data = request.get_json()
        if not data or 'email' not in data:
            return jsonify({'message': 'Email is required.'}), 400
        email = data.get('email')
        if uh.check_email(email):
            return jsonify({'message': 'No users match this email.'}), 400

        last_request_time = session.get('last_request_time')
        current_time = datetime.now()
        if last_request_time:
            last_request_time = datetime.strptime(last_request_time, '%Y-%m-%d %H:%M:%S.%f')
            if current_time < last_request_time + timedelta(seconds=email_timeout_duration):
                remaining_time = (last_request_time +
                                  timedelta(seconds=email_timeout_duration) -
                                  current_time).seconds
                return jsonify({'message': 'Please wait before sending another confirmation email.',
                                'remaining_time': remaining_time}), 429

        session['last_request_time'] = str(current_time)
        send_confirmation_code(email)
        session['password_reset_user'] = uh.fetch_user_by_email(email)
        return jsonify({'message': 'Email submitted successfully.'}), 200
    else:
        return redirect(url_for('home'))


@app.route('/submit-code', methods=['POST', 'GET'])
def submit_code():
    if request.method == 'POST':
        data = request.get_json()
        if not data or 'code' not in data:
            return jsonify({'message': 'Code is .'}), 400

        code = data.get('code')
        if code == session['confirmation_code']:
            session.pop('confirmation_code', None)

            return jsonify({'message': 'Code submitted successfully.'}), 200
        else:
            return jsonify({'message': 'Incorrect Code.'}), 400
    else:
        return redirect(url_for('home'))


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if 'password_reset_user' in session:
        return render_template('reset-password.html', logged_in=logged_in())
    else:
        return redirect(url_for('home'))


@app.route('/reset-password-redirect', methods=['POST', 'GET'])
def reset_password_redirect():
    if request.method == 'POST':
        data = request.get_json()

        if not data or 'password' not in data or 'confirm_password' not in data:
            return jsonify({'message': 'Please fill in all fields.'}), 400

        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if 'password_reset_user' in session:
            if password == confirm_password:
                if len(password) >= 10:
                    uh.update_password(session['password_reset_user'], data.get('password'))
                    session.pop('password_reset_user', None)
                    return jsonify({'message': 'Password successfully updated.'}), 200
                else:
                    return jsonify({'message': 'Password must be at least 10 characters long.'}), 400
            else:
                return jsonify({'message': 'Passwords do not match.'}), 400
        else:
            return jsonify({'message': 'User session not found or expired.'}), 400

    return redirect(url_for("home"))


@app.route('/profile')
def profile():
    return render_template("profile.html")


def logged_in():
    if 'logged_in' in session:
        return True
    else:
        return False


def send_confirmation_code(email):
    msg = Message('Email Confirmation', sender='no-reply@domain.com', recipients=[email])
    session.pop('confirmation_code', None)
    session['confirmation_code'] = str(randint(10000, 99999))
    msg.body = "Your email confirmation code is: " + session['confirmation_code']
    mail.send(msg)


# run the app
if __name__ == '__main__':
    app.run(debug=True)
