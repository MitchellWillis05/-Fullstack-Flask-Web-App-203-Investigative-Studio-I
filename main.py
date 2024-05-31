# import libraries and other files
from flask import Flask, render_template, request
import user_handler as uh
import password_handler as ph
import credential_validate as cv

# define app
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signup_redirect', methods=['GET', 'POST'])
def signup_redirect():
    validation = cv.credential_validation(request.form['username'], request.form['email'],
                                          request.form['password'], request.form['confirm_password'])

    if len(validation) > 0:
        return render_template('signup.html', error=validation)
    else:
        return "signup_redirect_pass"


# run the app
if __name__ == '__main__':
    app.run(debug=True)
