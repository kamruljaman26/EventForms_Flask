from flask import Flask, render_template, request
from flask import redirect, url_for, session, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta, time
import xlsxwriter
import os


app = Flask(__name__)
app.secret_key = 'asdfghjkppiuytrewqasdfghjk'  # secret_key session end-to-end encryption
app.permanent_session_lifetime = timedelta(days=3)
app.config["DEBUG"] = True


# SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(
    user='root',
    password='Kamrul1Himel',
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


# Create Excel File
def create_excel_file():
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, 'static/pdf/UserData.xlsx')

    workbook = xlsxwriter.Workbook(my_file)

    # Sheet1, Sheet2 etc., but we can also specify a name.
    worksheet = workbook.add_worksheet("User Data")

    # Start from the first cell. Rows and
    row = 0
    col = 0

    # Add Header
    worksheet.write(0, col, 'Name')
    worksheet.write(0, col + 1, 'Phone Numer')
    worksheet.write(0, col + 2, 'Email Address')
    worksheet.write(0, col + 3, 'NID/Pass')
    worksheet.write(0, col + 4, 'Total Participant')
    worksheet.write(0, col + 5, 'Session ID')

    # Update Row
    row += 1

    # Collect Data From DB
    result = db.session.query(User).all()

    for user in result:
        worksheet.write(row, col, user.name)
        worksheet.write(row, col + 1, user.phone)
        worksheet.write(row, col + 2, user.email)
        worksheet.write(row, col + 3, user.nid_pas_num)
        worksheet.write(row, col + 4, user.participant)
        worksheet.write(row, col + 5, user.session_id)
        row += 1

    workbook.close()


# Registration Form
@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        global message
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

                return render_template('successful.html')
            except Exception as e:
                if phone in e.__str__():
                    message = phone + " this phone number already used for registration," \
                                      " please try with different phone number."

                if email in e.__str__():
                    message = email + " this email address already used for registration," \
                                      " please try with different email address."

                if phone in e.__str__():
                    message = passport_no + " this Passport/NID number already used for registration," \
                                            " please try with different Passport/NID number."

                return render_template('index.html', err_alert=True, err_message=message)

    elif request.method == 'GET':
        return render_template('index.html')


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
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'GET':
        try:
            if not session['admin_email']:
                return redirect(url_for('admin'))
        except:
            return render_template('login.html')
        else:
            create_excel_file()
            return render_template('dashboard.html')
    elif request.method == 'POST':
        try:
            num_rows_deleted = db.session.query(User).delete()
            print(num_rows_deleted)
            db.session.commit()
            return render_template('dashboard.html', is_delete=True, message=message)
        except Exception as e:
            db.session.rollback()
            message = 'Something error!'
            return render_template('dashboard.html', is_delete=True, message=message)


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


# Download PDF List
@app.route('/api/download-excel', methods=['POST'])
def download_excel():
    path = 'static/pdf/UserData.xlsx'
    return send_file(path, as_attachment=True)


# Delete All User Data
@app.route('/api/delete-user-data', methods=['POST'])
def delete_user_data():
    pass


# Main Function
if __name__ == "__main__":
    app.run(debug=True)
