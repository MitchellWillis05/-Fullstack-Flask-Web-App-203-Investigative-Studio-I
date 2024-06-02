# import libraries and other files
import werkzeug.exceptions
from flask import Flask, render_template, request
import user_handler as uh
import password_handler as ph
import credential_validate as cv

# define app
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html', logged_in=logged_in)


@app.route('/login')
def login():
    return render_template('login.html', logged_in=logged_in)


@app.route('/login_redirect', methods=['GET', 'POST'])
def login_redirect():
    try:
        if uh.validate_login(request.form['email'], request.form['password']):

            return "login redirect pass"
        else:
            return render_template("login.html", error="Incorrect username / password", logged_in=logged_in)
    except werkzeug.exceptions.BadRequest as er:
        return render_template("login.html", error="Please fill out all fields", logged_in=logged_in)


@app.route('/signup')
def signup():
    return render_template('signup.html', logged_in=logged_in)


@app.route('/signup_redirect', methods=['GET', 'POST'])
def signup_redirect():
    try:
        validation = cv.credential_validation(request.form['username'], request.form['email'],
                                              request.form['password'], request.form['confirm_password'])
    except werkzeug.exceptions.BadRequest as e:
        validation = "Please fill out all fields"

    if len(validation) > 0:
        return render_template('signup.html', error=validation, logged_in=logged_in)
    else:
        return render_template('login.html', error=validation, logged_in=logged_in)


# run the app
if __name__ == '__main__':
    app.run(debug=True)
