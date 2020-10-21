from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:JAMANkamrul1@@localhost/eventforms'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route("/")
def index():
    return 'Hello'


if __name__ == "__main__":
    app.run(debug=True)