# import libraries and other files
import openai
from dotenv import load_dotenv
import os
from random import randint
from openai import OpenAI
import werkzeug.exceptions
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mail import Mail, Message
import user_handler as uh
import password_handler as ph
import credential_validate as cv
import starsign_data as sd
import journal_handler as jh
from datetime import datetime, timedelta
from PIL import Image

load_dotenv()

# define app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'lucid.log.confirmations@gmail.com'
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

UPLOAD_FOLDER = 'static/images/profile-pictures'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

api_key = 'sk-proj-2qqKxg8EM0oUW54B3EX0T3BlbkFJy3GTBsB1BGVKTtTeKg1Y'
if api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable not set")
else:
    client = OpenAI(api_key=api_key)

email_timeout_duration = 60 * 2


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', logged_in=logged_in()), 404


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return jsonify({'message': 'Method not allowed.'}), 405
    elif request.method == 'GET':
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
            if 'signup_user_verified' not in session:
                return jsonify({'message': "There was an error creating your account."}), 400
            else:
                encrypted_password = ph.encrypt_password(request.form['password'])
                uh.create_new_user(request.form['username'], request.form['email'], encrypted_password,
                                   request.form['dob_day'], request.form['dob_month'], request.form['dob_year'],
                                   cv.get_star_sign(int(request.form['dob_day']), int(request.form['dob_month'])),
                                   request.form['selected_gender'])
                return jsonify({'message': 'Signup Successful.'}), 200
        except werkzeug.exceptions.BadRequest:
            return jsonify({'message': 'Please fill in all fields.'}), 400
        except ValueError:
            return jsonify({'message': 'Please fill in all fields.'}), 400

    elif request.method == 'GET':
        session.pop('signup_user_validated', None)
        session.pop('signup_user_verified', None)
        if logged_in():
            return redirect(url_for('home'))
        else:
            return render_template('signup.html', logged_in=logged_in())


@app.route('/submit-forgot-email', methods=['GET', 'POST'])
def submit_forgot_email():
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
                    else:
                        pass

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


@app.route('/submit-signup-email', methods=['GET', 'POST'])
def submit_signup_email():
    session.pop('password_reset_user', None)
    if request.method == 'POST':
        try:
            email = request.form['email']
            validation = cv.credential_validation(request.form['username'], email,
                                                  request.form['password'], request.form['confirm_password'],
                                                  request.form['dob_year'], request.form['dob_month'],
                                                  request.form['dob_day'], request.form['selected_gender'])
            print(validation)
            if validation is not None:
                return jsonify({'message': validation}), 400
            last_request_time = session.get('last_request_time')
            current_time = datetime.now()
            if last_request_time:
                last_request_time = datetime.strptime(last_request_time, '%Y-%m-%d %H:%M:%S.%f')
                if current_time < last_request_time + timedelta(seconds=email_timeout_duration):
                    remaining_time = (last_request_time +
                                      timedelta(seconds=email_timeout_duration) -
                                      current_time).seconds
                    print("WAIT")
                    return jsonify({'message': 'Please wait before sending another confirmation email.',
                                    'remaining_time': remaining_time}), 429
                else:
                    pass

            session['last_request_time'] = str(current_time)
            send_confirmation_code(email)
            session['signup_user_validated'] = True
            return jsonify({'message': 'Success.'}), 200

        except werkzeug.exceptions.BadRequest:
            return jsonify({'message': 'Please fill all fields.'}), 400
    else:
        return redirect(url_for('home'))


@app.route('/submit-code', methods=['POST', 'GET'])
def submit_code():
    if request.method == 'POST':
        try:
            code = request.form['code-input']
            if code == session['confirmation_code']:
                session.pop('confirmation_code', None)
                if 'signup_user_validated' in session:
                    session.pop('signup_user_validated', None)
                    session['signup_user_verified'] = True
                return jsonify({'message': 'Code submitted successfully.'}), 200
            else:
                return jsonify({'message': 'Incorrect Code.'}), 400
        except werkzeug.exceptions.BadRequest:
            return jsonify({'message': 'Please enter code.'}), 400
    elif request.method == 'GET':
        return redirect(url_for('home'))


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        try:
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            if 'password_reset_user' in session:
                if password == confirm_password:
                    if len(password) >= 10:
                        uh.update_password(session['password_reset_user'], password)
                        session.pop('password_reset_user', None)
                        return jsonify({'message': 'Password successfully updated.'}), 200
                    else:
                        return jsonify({'message': 'Password must be at least 10 characters long.'}), 400
                else:
                    return jsonify({'message': 'Passwords do not match.'}), 400
            else:
                return jsonify({'message': 'User session not found or expired.'}), 400
        except werkzeug.exceptions.BadRequest:
            return jsonify({'message': 'Please fill in all fields.'}), 400
        except ValueError:
            return jsonify({'message': 'Please fill in all fields.'}), 400
    elif request.method == 'GET':
        if 'password_reset_user' in session:
            return render_template('reset-password.html', logged_in=logged_in())
        else:
            return redirect(url_for('home'))


@app.route('/profile', methods=['GET'])
def profile():
    if request.method == 'GET':
        session.pop('password_reset_user', None)
        if logged_in():
            user_id = str(session['current_user_logged_in'])
            user_image_filename = get_user_image_filename(user_id)
            if user_image_filename:
                user_image_url = url_for('static', filename=f'images/profile-pictures/{user_image_filename}')
            else:
                user_image_url = None
            print("xxx")
            print(user_image_url)
            data = uh.fetch_cred_by_id(user_id)
            # username = 0 email = 1 day = 2 month = 3 year = 4 starsign = 5 gender = 6
            if len(str(data[3])) == 1:
                dob = str(data[2]) + '/0' + str(data[3]) + '/' + str(data[4])
            else:
                dob = str(data[2]) + '/' + str(data[3]) + '/' + str(data[4])
            starsign_data = sd.get_starsign_info(data[5])
            return render_template("profile.html", username=data[0], email=data[1],
                                   gender=data[6], dob=dob, starsign=data[5], s_desc=starsign_data,
                                   logged_in=logged_in(), user_image_url=user_image_url)
        return redirect(url_for('login'))
    else:
        return redirect(url_for('home'))


@app.route('/journal', methods=['GET', 'POST'])
def journal():
    if request.method == 'POST':
        try:
            title = request.form['title']
            mood = request.form['mood']
            color = request.form['color']
            content = request.form['content']
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
        except werkzeug.exceptions.BadRequest:
            return jsonify({'message': 'Please fill in all fields.'}), 400
        except ValueError:
            return jsonify({'message': 'Please fill in all fields.'}), 400

    elif request.method == 'GET':
        if logged_in():
            entry_data = jh.fetch_entries_by_userid(session['current_user_logged_in'])
            return render_template('journal.html', logged_in=logged_in(), entry_data=jh.get_journal_preview(entry_data))
        return redirect(url_for('login'))


@app.route('/entry/<entryid>', methods=['GET', 'POST'])
def entry(entryid):
    if request.method == 'POST':
        if logged_in():
            if jh.fetch_entry_by_entryid(entryid) is not None:
                selected_entry = jh.fetch_entry_by_entryid(entryid)
                if selected_entry[0] == session['current_user_logged_in']:
                    prompt_available = jh.check_generation_vacancy(entryid)
                    if prompt_available is None:

                        try:
                            ai_prompt = generate_ai_analysis(selected_entry)
                        except openai.AuthenticationError:
                            return jsonify(
                                {'message': "AI Generation is not currently available, please try again later."}), 503
                        if ai_prompt is not None:
                            uh.new_request(selected_entry[0])
                            jh.enter_generation_into_entry(ai_prompt, entryid)
                            return jsonify({'message': ai_prompt}), 200
                        else:
                            return jsonify({'message': "Please wait before generating another response."}), 400
                    else:
                        return jsonify({'message': "You have already generated a response for this entry."}), 400
            return jsonify({'message': 'You do not have access to this entry.'}), 401
    elif request.method == 'GET':
        if logged_in():
            if jh.fetch_entry_by_entryid(entryid) is not None:
                selected_entry = jh.fetch_entry_by_entryid(entryid)
                ai_data = jh.check_generation_vacancy(entryid)
                if ai_data is None:
                    ai_data = ""
                if selected_entry[0] == session['current_user_logged_in']:
                    return render_template('journal-entry.html',
                                           entry_data=selected_entry, logged_in=logged_in(), entryid=entryid,
                                           ai_data=ai_data)
        return redirect(url_for('journal'))


@app.route('/delete-entry', methods=['GET', 'POST'])
def delete_entry():
    if request.method == 'POST':
        try:
            entryid = request.form['entry_id']
        except werkzeug.exceptions.BadRequest:
            return jsonify({'message': 'No entry selected.'}), 400
        if logged_in():
            if jh.fetch_entry_by_entryid(entryid) is not None:
                selected_entry = jh.fetch_entry_by_entryid(entryid)
                if selected_entry[0] == session['current_user_logged_in']:
                    if jh.delete_entry_by_entryid(entryid):
                        return jsonify({'message': 'Deleted entry.'}), 200
                    return jsonify({'message': 'There was an error deleting the entry.'}), 400
        return jsonify({'message': 'You do not have access to this entry.'}), 400
    elif request.method == 'GET':
        return redirect(url_for('journal'))


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'current_user_logged_in' in session:
            if 'file' not in request.files:
                return jsonify({'message': 'File not found.'}), 400
            file = request.files['file']
            if file.filename == '':
                return jsonify({'message': 'Invalid file name.'}), 400
            if file and allowed_file(file.filename):
                user_id = str(session.get('current_user_logged_in'))
                original_extension = file.filename.rsplit('.', 1)[1].lower()
                base_filename = user_id
                filename = f"{base_filename}.{original_extension}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                delete_existing_files(app.config['UPLOAD_FOLDER'], base_filename)

                file.save(file_path)

                with Image.open(file_path) as img:
                    if img.size[0] > 200 or img.size[1] > 200:
                        img.thumbnail((200, 200))
                        img.save(file_path)

                return jsonify({'message': 'File uploaded successfully.'}), 200
            else:
                return jsonify({'message': 'Invalid file.'}), 400
        else:
            return jsonify({'message': 'Unauthorized access.'}), 401
    else:
        return redirect(url_for('profile'))


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


def generate_ai_analysis(selected_entry):
    if 'current_user_logged_in' in session:
        last_request_time_str = uh.fetch_last_request(session['current_user_logged_in'])
        if last_request_time_str:
            last_request_time = datetime.strptime(last_request_time_str, "%Y-%m-%d %H:%M:%S")

            current_time = datetime.now()

            time_difference = current_time - last_request_time

            if time_difference > timedelta(minutes=5):
                pass
            else:
                print(current_time, last_request_time)
                return None
        else:
            pass

        title = selected_entry[1]
        mood = selected_entry[2]
        color = selected_entry[3]
        content = selected_entry[4]
        starsign = uh.fetch_prompt_info_by_userid(session['current_user_logged_in'])[0]
        gender = uh.fetch_prompt_info_by_userid(session['current_user_logged_in'])[1]
        prompt = ("generate an analysis/explanation for my dream, "
                  "the title of my dream is: " + title
                  + ". The emotion I felt most in my dream was: " + mood
                  + ". The color I associate my dream with is: " + color
                  + ". This is what happened in my dream: " + content
                  + ". My starsign is: " + starsign
                  + ". And my gender is: " + gender
                  + ". Please generate an analysis/explanation for my dream taking this information into account. "
                    "Only use the starsign and/or gender if it is relevant"
                    " MAX 300 CHARACTERS."
                  )
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo",
        )
        return chat_completion.choices[0].message.content
    return None


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def delete_existing_files(directory, base_filename):
    for filename in os.listdir(directory):
        if filename.rsplit('.', 1)[0] == base_filename:
            os.remove(os.path.join(directory, filename))


def get_user_image_filename(user_id):
    for filename in os.listdir(UPLOAD_FOLDER):
        if filename.startswith(user_id):
            return filename
    return None

# run the app
if __name__ == '__main__':
    app.run(debug=True)
