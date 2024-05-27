# import libraries and other files
from flask import Flask, render_template, request
import user_handler
import password_handler

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
    username_data = request.form['username']
    email_data = request.form['email']
    password_data = password_handler.encrypt_password(request.form['password'])
    NL_data = request.form['NL']
    if password_handler.verify_password(request.form['confirm_password'], password_data):
        if len(request.form['confirm_password']) >= 10:
            return "signup_redirect success"
        else:
            return "signup_redirect fail"
    else:
        return "signup_redirect fail"


# run the app
if __name__ == '__main__':
    app.run(debug=True)
