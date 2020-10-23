from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.secret_key = 'asdfghjkppiuytrewqasdfghjk'  # secret_key session end-to-end encryption
app.permanent_session_lifetime = timedelta(days=3)

# SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(
    user='root',
    password='JAMANkamrul1@',
    server='localhost',
    database='eventforms'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database
db = SQLAlchemy(app)


# Admin/Super User Model Class
class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, name, email, phone, password):
        self.name = name
        self.email = email
        self.phone = phone
        self.password = password


# Registration Form Model Class
class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True,nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    nid_pas_num = db.Column(db.String(100), nullable=False)
    participant = db.Column(db.Integer, nullable=False)
    session_id = db.Column(db.String(20), db.ForeignKey('session.session_id'))

    def __init__(self, user_id, name, email, nid_pass_num, participant):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.nid_pas_num = nid_pass_num
        self.participant = participant


# Session Form Model
class Session(db.Model):
    __tablename__ = 'session'
    session_id = db.Column(db.String(20), primary_key=True)
    session_name = db.Column(db.String(200), nullable=False)
    session_date = db.Column(db.Date, nullable=False)
    session_time = db.Column(db.Time, nullable=False)
    seat_booked = db.Column(db.Integer, nullable=False, default=0)
    children = relationship("user")

    def __init__(self, session_id, session_name, session_date, session_time):
        self.session_id = session_id
        self.session_name = session_name
        self.session_date = session_date
        self.session_time = session_time


# Registration Form
@app.route("/")
def index():
    return render_template('index.html')


# Admin Login
@app.route("/admin", methods=['POST', 'GET'])
def admin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Collect data from DB
        query = db.session.query(Admin.name, Admin.email, Admin.password).filter(Admin.email.in_([email, ]))
        results = query.all()

        if results and results[0][2] == password:
            # create session
            session['admin_name'] = results[0][0]
            session['admin_email'] = email  # User Name
            session['admin_phone'] = password  # User Phone Number
            session.permanent = True

            return redirect(url_for('dashboard'))
        else:
            message = 'Email or Password is not correct, Please try again.'
            return render_template('login.html', message=message)

    elif request.method == 'GET':
        try:
            if session['admin_email']:
                return redirect(url_for('dashboard'))
        except:
            return render_template('login.html')
        return render_template('login.html')


# Admin Dashboard
@app.route('/dashboard')
def dashboard():
    try:
        if not session['admin_email']:
            return redirect(url_for('admin'))
    except:
        return render_template('login.html')
    else:
        # todo
        return render_template('dashboard.html')


# Log out
@app.route('/logout')
def logout():
    # Delete session data
    session.pop('admin_name', None)
    session.pop('admin_email', None)
    session.pop('admin_phone', None)
    return redirect(url_for('admin'))


# Main Function
if __name__ == "__main__":
    app.run(debug=True)