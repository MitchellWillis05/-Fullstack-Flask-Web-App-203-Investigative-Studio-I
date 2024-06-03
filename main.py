# import libraries and other files
import os
import werkzeug.exceptions
from flask import Flask, render_template, request, redirect, url_for, session
import user_handler as uh
import password_handler as ph
import credential_validate as cv

# define app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['REMEMBER_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['REMEMBER_COOKIE_HTTPONLY'] = True


@app.route('/')
def home():

    return render_template('home.html', logged_in=logged_in())


@app.route('/login')
def login():
    if logged_in():
        return redirect(url_for('home'))
    return render_template('login.html', logged_in=logged_in())


@app.route('/login_redirect', methods=['GET', 'POST'])
def login_redirect():
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
    if logged_in():
        return redirect(url_for('home'))
    return render_template('signup.html', logged_in=logged_in())


@app.route('/signup_redirect', methods=['GET', 'POST'])
def signup_redirect():
    try:
        validation = cv.credential_validation(request.form['username'], request.form['email'],
                                              request.form['password'], request.form['confirm_password'])
    except werkzeug.exceptions.BadRequest as e:
        return redirect(url_for("login"))

    if len(validation) > 0:
        return render_template('signup.html', error=validation, logged_in=logged_in())
    else:
        return render_template('login.html', error=validation, logged_in=logged_in())


def logged_in():
    if 'logged_in' in session:
        return True
    else:
        return False


# run the app
if __name__ == '__main__':
    app.run(debug=True)
