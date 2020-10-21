from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SqlAlchemy Database Configuration With Mysql
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:JAMANkamrul1@@localhost/eventforms'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(
    user='root', password='JAMANkamrul1@', server='localhost', database='eventforms')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database
db = SQLAlchemy(app)


# Admin/Super User Model Class
class Admin(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone


# Registration Form Model Class
class UserForm(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True,nullable=False)


# Registration Form
@app.route("/")
def index():
    return render_template('index.html')


# Admin Login
@app.route("/admin")
def admin():
    return render_template('login.html')


# Admin Dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


if __name__ == "__main__":
    app.run(debug=True)