# import libraries and other files
import os
from random import randint

import werkzeug.exceptions
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mail import Mail, Message
import user_handler as uh
import credential_validate as cv
import starsign_data as sd
import journal_handler as jh
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    session.pop('password_reset_user', None)
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            if cv.email_validator(email):
                if uh.validate_login(email, password):
                    session["current_user_logged_in"] = uh.fetch_user_by_email(email)
                    return jsonify({'message': 'login Successful.'}), 200
                else:
                    return jsonify({'message': 'Email or password is incorrect.'}), 400
            else:
                return jsonify({'message': 'Invalid email.'}), 400
        except werkzeug.exceptions.BadRequest:
            return jsonify({'message': 'Please fill in all fields.'}), 400

    elif request.method == 'GET':
        if logged_in():
            return redirect(url_for('home'))
        else:
            return render_template('login.html', logged_in=logged_in())


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    session.pop('password_reset_user', None)
    if request.method == 'POST':
        try:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            dob_day = request.form['dob_day']
            dob_month = request.form['dob_month']
            dob_year = request.form['dob_year']
            gender = request.form['gender']
            validation = cv.credential_validation(username, email,
                                                  password, confirm_password,
                                                  dob_year, dob_month, dob_day, gender)

            if len(validation) > 0:
                return jsonify({'message': validation}), 400
            else:
                return jsonify({'message': 'Signup Successful.'}), 200
        except werkzeug.exceptions.BadRequest:
            return jsonify({'message': 'Please fill in all fields.'}), 400
        except ValueError:
            return jsonify({'message': 'Please fill in all fields.'}), 400

    elif request.method == 'GET':
        if logged_in():
            return redirect(url_for('home'))
        else:
            return render_template('signup.html', logged_in=logged_in())


@app.route('/submit-email', methods=['GET', 'POST'])
def submit_email():
    session.pop('password_reset_user', None)
    if request.method == 'POST':
        try:
            email = request.form['email-input']
            if cv.email_validator(email):
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
                return jsonify({'message': 'Invalid email.'}), 400

        except werkzeug.exceptions.BadRequest:
            return jsonify({'message': 'Please enter email.'}), 400
    else:
        return redirect(url_for('home'))


@app.route('/submit-code', methods=['POST', 'GET'])
def submit_code():
    if request.method == 'POST':
        try:
            code = request.form['code-input']
            if code == session['confirmation_code']:
                session.pop('confirmation_code', None)
                return jsonify({'message': 'Code submitted successfully.'}), 200
            else:
                return jsonify({'message': 'Incorrect Code.'}), 400
        except werkzeug.exceptions.BadRequest:
            return jsonify({'message': 'Please enter code.'}), 400
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
        try:
            data = request.get_json()

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
        except ValueError:
            return jsonify({'message': 'Please fill in all fields.'}), 400

    return redirect(url_for("home"))


@app.route('/profile')
def profile():
    session.pop('password_reset_user', None)
    if logged_in():
        data = uh.fetch_cred_by_id(session['current_user_logged_in'])
        # username = 0 email = 1 day = 2 month = 3 year = 4 starsign = 5 gender = 6
        if len(str(data[3])) == 1:
            dob = str(data[2]) + '/0' + str(data[3]) + '/' + str(data[4])
        else:
            dob = str(data[2]) + '/' + str(data[3]) + '/' + str(data[4])
        starsign_data = sd.get_starsign_info(data[5])
        return render_template("profile.html", username=data[0], email=data[1],
                               gender=data[6], dob=dob, starsign=data[5], s_desc=starsign_data, logged_in=logged_in())
    return redirect(url_for('home'))


@app.route('/journal', methods=['GET', 'POST'])
def journal():
    if request.method == 'POST':
        try:
            data = request.get_json()
            title = data.get('title')
            mood = data.get('mood')
            color = data.get('color')
            content = data.get('content')
            print(mood)
            date = datetime.now().strftime('%m/%d/%Y')
            if cv.journal_validate(title, mood, color, content) == 1:
                return jsonify({'message': 'Invalid title length.'}), 400
            if cv.journal_validate(title, mood, color, content) == 2:
                return jsonify({'message': 'Please select a mood.'}), 400
            if cv.journal_validate(title, mood, color, content) == 3:
                return jsonify({'message': 'Please select a color.'}), 400
            if cv.journal_validate(title, mood, color, content) == 4:
                return jsonify({'message': 'Invalid content length.'}), 400
            user_id = session['current_user_logged_in']
            if jh.create_new_entry(user_id, title, mood, color, content, date):
                return jsonify({'message': 'Successfully created entry.'}), 200
            return jsonify({'message': 'An error occurred.'}), 400

        except ValueError:
            return jsonify({'message': 'Please fill in all fields.'}), 400

    if logged_in():
        entry_data = jh.fetch_entries_by_id(session['current_user_logged_in'])
        return render_template('journal.html', logged_in=logged_in(), entry_data=jh.get_journal_preview(entry_data))
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.pop('password_reset_user', None)
    session.pop('current_user_logged_in', None)
    return redirect(url_for('login'))


def logged_in():
    if 'current_user_logged_in' in session:
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
