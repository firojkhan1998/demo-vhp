from flask_migrate import Migrate
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///demo.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Demo(db.Model):
    id = db.Column(db.Integer, auto_increment=True, primary_key=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.DateTime, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    degree = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"{self.id} - {self.fname} - {self.lname} - {self.dob} - {self.email} - {self.contact} - {self.degree} - {self.address}"

@app.route('/provider_create', methods=["GET", "POST"])
def provider_create():
    if request.method == "POST":
        fname = request.form['firstname']
        lname = request.form['lastname']
        dob = request.form['dob']
        email = request.form['email']
        contact = request.form['phone']
        degree = request.form['degree']
        address = request.form['address']
        dob = datetime.strptime(dob, "%Y-%m-%d")

        new_demo = Demo(
            fname=fname,
            lname=lname,
            dob=dob,
            email=email,
            contact=contact,
            degree=degree,
            address=address
        )
        db.session.add(new_demo)
        db.session.commit()
        return render_template('provider_create.html', message="Provider information saved successfully!")
    return render_template('provider_create.html') 


@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route('/provider_view')
def provider_view():
    allnew_demo = Demo.query.all()
    print(allnew_demo)
    return render_template('provider_view.html', demo=allnew_demo)


@app.route("/welcome/<name>")
def welcome_name(name):
    return "<h1>Welcome " + name +" !</h1>"


if __name__ == "__main__":
    app.run(debug=True)
