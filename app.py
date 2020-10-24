from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'asdfghjkppiuytrewqasdfghjk'  # secret_key session end-to-end encryption
app.permanent_session_lifetime = timedelta(days=3)
app.config["DEBUG"] = True

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
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, name, email, phone, password):
        self.name = name
        self.email = email
        self.phone = phone
        self.password = password

    def __repr__(self):
        return f"({self.admin_id},{self.name},{self.email},{self.password}"


# Registration Form Model Class
class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    nid_pas_num = db.Column(db.String(100), nullable=False, unique=True)
    participant = db.Column(db.Integer, nullable=False)
    session_id = db.Column(db.String(20), db.ForeignKey('session.session_id'))

    def __init__(self, name, phone, email, nid_pass_num, participant, session_id):
        self.name = name
        self.phone = phone
        self.email = email
        self.nid_pas_num = nid_pass_num
        self.participant = participant
        self.session_id = session_id

    def __repr__(self):
        return f"({self.user_id},{self.name},{self.phone},{self.email},{self.nid_pas_num}," \
               f"{self.participant},{self.session_id})"


# Session Form Model
class Session(db.Model):
    __tablename__ = 'session'
    session_id = db.Column(db.String(20), primary_key=True)
    session_name = db.Column(db.String(200), nullable=False)
    session_date = db.Column(db.Date, nullable=False)
    session_time = db.Column(db.Time, nullable=False)
    seat_booked = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, session_id, session_name, session_date, session_time):
        self.session_id = session_id
        self.session_name = session_name
        self.session_date = session_date
        self.session_time = session_time

    def __repr__(self):
        return f"({self.session_id},{self.session_name},{self.session_date}, {self.session_time}, {self.seat_booked})"

    def __str__(self):
        directory = dict(
            session_id=self.session_id,
            session_name=self.session_name,
            session_date=str(self.session_date),
            session_time=str(self.session_time),
            seat_booked=self.seat_booked
        )
        # my_list = (self.session_id, self.session_name,str(self.session_date),str(self.session_time),self.seat_booked)
        return directory


# Registration Form
@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        return render_template('index.html')


# Submit Registration
@app.route('/reg', methods=['POST', 'GET'])
def reg():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        passport_no = request.form.get('passport_no')
        total_person = int(request.form.get('total_person'))
        time_slot = request.form.get('time_slot')

        try:
            user = User(name, phone, email, passport_no, total_person, time_slot)
            session = db.session
            session.add(user)
            session.commit()
            print(time_slot)

            # Update data in Session
            sec_session = Session.query.filter_by(session_id=time_slot).first()
            sec_session.seat_booked = sec_session.seat_booked + total_person
            session.commit()

            return 'Registration Successful'
        except Exception as e:
            return jsonify(e.__str__())


# Admin Login
@app.route("/admin", methods=['POST', 'GET'])
def admin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Collect data from DB
        results = db.session.query(Admin.name, Admin.email, Admin.password) \
            .filter(Admin.email.in_([email, ])).all()

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
        return render_template('dashboard.html')


# Log out
@app.route('/logout')
def logout():
    # Delete session data
    session.pop('admin_name', None)
    session.pop('admin_email', None)
    session.pop('admin_phone', None)
    return redirect(url_for('admin'))


# Convert INTO LIST
def convert_to_list(values):
    my_dit = {}
    some = []
    for x in values:
        some.append(x.__str__())
    my_dit['list'] = some
    return some


# Get Session/Time : API
@app.route('/api/get-slot', methods=['GET'])
def get_time_slot():
    if 'date' in request.args:
        date = str(request.args['date'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Collect data from DB
    time_list = Session.query.filter(Session.session_date.in_([date, ])).all()
    return jsonify(convert_to_list(time_list))


# Main Function
if __name__ == "__main__":
    app.run(debug=True)
