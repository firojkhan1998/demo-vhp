from flask_migrate import Migrate
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///demo.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Demo(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.DateTime, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    degree = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"{self.id} - {self.fname} - {self.lname} - {self.dob} - {self.email} - {self.contact} - {self.degree} - {self.address}"

class Patient(db.Model):
    patient_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    patient_fname = db.Column(db.String(100), nullable=False)
    patient_lname = db.Column(db.String(100), nullable=False)
    patient_dob = db.Column(db.DateTime, nullable=False)
    patient_aadhar = db.Column(db.Integer, nullable=False)
    patient_email = db.Column(db.String(100), nullable=False)
    patient_contact = db.Column(db.String(15), nullable=False)
    patient_address = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"{self.patient_id} - {self.patient_fname} - {self.patient_lname} - {self.patient_dob} - {self.patient_aadhar} - {self.patient_email} - {self.patient_contact} - {self.patient_address}"

class Hospital(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    hospital_name = db.Column(db.String(100), nullable=False)
    hospital_company_name = db.Column(db.String(100), nullable=False)
    hospital_email = db.Column(db.String(100), nullable=False)
    hospital_contact = db.Column(db.String(15), nullable=False)
    hospital_address = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"{self.id} - {self.hospital_name} - {self.hospital_company_name} - {self.hospital_email} - {self.hospital_contact} - {self.hospital_address}"


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


@app.route('/provider_view')
def provider_view():
    allnew_demo = Demo.query.all()
    return render_template('provider_view.html', demo=allnew_demo)


@app.route('/patient_create', methods=["GET", "POST"])
def patient_create():
    if request.method == "POST":
        patient_fname = request.form['patient_fname']
        patient_lname = request.form['patient_lname']
        patient_dob = request.form['patient_dob']
        patient_aadhar = request.form['patient_aadhar']
        patient_email = request.form['patient_email']
        patient_contact = request.form['patient_contact']
        patient_address = request.form['patient_address']

        patient_dob = datetime.strptime(patient_dob, "%Y-%m-%d")

        new_patient = Patient(
            patient_fname=patient_fname,
            patient_lname=patient_lname,
            patient_dob=patient_dob,
            patient_aadhar=patient_aadhar,
            patient_email=patient_email,
            patient_contact=patient_contact,
            patient_address=patient_address,
        )
        db.session.add(new_patient)
        db.session.commit()
        return render_template('patient_create.html', message="Patient information saved successfully!")
    return render_template('patient_create.html')


@app.route('/patient_view')
def patient_view():
    allnew_patient = Patient.query.all()
    return render_template('patient_view.html', new_patient=allnew_patient)


@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/hospital_create")
def hospital_create():    
    if request.method == "POST":
        hospital_name = request.form['hospital_fname']
        Company_name = request.form['hospital_lname']
        hospital_email = request.form['hospital_email']
        hospital_contact = request.form['hospital_contact']
        hospital_address = request.form['hospital_address']

        new_hospital = Patient(
            hospital_name=hospital_name,
            Company_name=Company_name,
            hospital_email=hospital_email,
            hospital_contact=hospital_contact,
            hospital_address=hospital_address
        )
        db.session.add(new_hospital)
        db.session.commit()
        return render_template('hospital_create.html', message="Hospital information saved successfully!")
    return render_template('hospital_create.html')


@app.route('/hospital_view')
def hospital_view():
    allnew_hospital = Hospital.query.all()
    return render_template('hospital_view.html', new_hospital=allnew_hospital)


@app.route("/welcome/<name>")
def welcome_name(name):
    return f"<h1>Welcome {name}!</h1>"


if __name__ == "__main__":
    app.run(debug=True)
