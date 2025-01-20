from flask_migrate import Migrate
from flask import Flask, flash, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt
import os


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///demo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret_key'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(100), unique=True)
    user_password = db.Column(db.String(100))

    def __init__(self,email,password,name):
        self.user_name = name
        self.user_email = email
        self.user_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.user_password.encode('utf-8'))
    
        
@app.route("/")
@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user_email = request.form['email']
        user_password = request.form['password']

        user = User.query.filter_by(user_email=user_email).first()

        if user and user.check_password(user_password):
            session['email'] = user.user_email
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Invalid User!')
    return render_template('login.html')

@app.route("/registration", methods=['GET','POST'])
def registration():
    if request.method == 'POST':
        user_name = request.form['name']
        user_email = request.form['email']
        user_password = request.form['password']

        new_user = User(email=user_email, password=user_password, name=user_name)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template('registration.html')

# @app.route("/")
# def hello_world():
#     return render_template('index.html')


@app.route("/dashboard")
def dashboard():
    if 'email' in session:
        count = Demo.query.count()
        patient_count = Patient.query.count()
        hospital_count = Hospital.query.count()
        return render_template('dashboard.html', count=count, patient_count=patient_count, hospital_count=hospital_count )
    return redirect('/login')


@app.route("/visit_view")
def visit_view():
    return render_template('visit_view.html')


@app.route("/visit_create")
def visit_create():
    return render_template('visit_create.html')


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
        return redirect(url_for('provider_view'))
    return render_template('provider_create.html')


@app.route('/provider_view')
def provider_view():
    allnew_demo = Demo.query.all()
    count = Demo.query.count()
    return render_template('provider_view.html', demo=allnew_demo, count=count)


@app.route("/delete/<int:id>")
def delete(id):
    demo = Demo.query.filter_by(id=id).first()
    if demo:
        db.session.delete(demo)
        db.session.commit()
    return redirect(url_for('provider_view'))


@app.route("/provider_update/<int:id>", methods=["GET", "POST"])
def provider_update(id):
    demo = Demo.query.filter_by(id=id).first()
    if demo:
        if request.method == "POST":
            demo.fname = request.form.get('firstname')
            demo.lname = request.form.get('lastname')
            demo.dob = datetime.strptime(request.form.get('dob'), "%Y-%m-%d")
            demo.email = request.form.get('email')
            demo.contact = request.form.get('phone')
            demo.degree = request.form.get('degree')
            demo.address = request.form.get('address')

            db.session.commit()

            return redirect(url_for('provider_view'))
    return render_template('provider_edit.html', demo=demo)


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

        patient_name = patient_fname + " " + patient_lname

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
        return redirect(url_for('patient_view', patient_name=patient_name))
    return render_template('patient_create.html')


@app.route("/patient_update/<int:patient_id>", methods=["GET", "POST"])
def patient_update(patient_id):
    patient = Patient.query.filter_by(patient_id=patient_id).first()
    if patient:
        if request.method == "POST":
            patient.patient_fname = request.form.get('patient_fname')
            patient.patient_lname = request.form.get('patient_lname')
            patient.patient_dob = datetime.strptime(request.form.get('patient_dob'), "%Y-%m-%d")
            patient.patient_aadhar = request.form.get('patient_aadhar')
            patient.patient_email = request.form.get('patient_email')
            patient.patient_contact = request.form.get('patient_contact')
            patient.patient_address = request.form.get('patient_address')

            db.session.commit()
            return redirect(url_for('patient_view'))
    return render_template('patient_edit.html', patient=patient)


@app.route('/patient_view')
def patient_view():
    allnew_patient = Patient.query.all()
    patient_count = Patient.query.count()
    return render_template('patient_view.html', new_patient=allnew_patient, patient_count=patient_count)


@app.route("/delete/patient/<int:patient_id>")
def delete_patient(patient_id):
    patient = Patient.query.filter_by(patient_id=patient_id).first()
    if patient:
        db.session.delete(patient)
        db.session.commit()
    return redirect(url_for('patient_view'))


class Hospital(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    hospital_name = db.Column(db.String(100), nullable=False)
    hospital_company_name = db.Column(db.String(100), nullable=False)
    hospital_email = db.Column(db.String(100), nullable=False)
    hospital_contact = db.Column(db.String(15), nullable=False)
    hospital_address = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"{self.id} - {self.hospital_name} - {self.hospital_company_name} - {self.hospital_email} - {self.hospital_contact} - {self.hospital_address}"


@app.route("/hospital_create", methods=['GET', 'POST'])
def hospital_create():    
    if request.method == "POST":
        hospital_name = request.form['hospital_name']
        hospital_company_name = request.form['hospital_company_name']
        hospital_email = request.form['hospital_email']
        hospital_contact = request.form['hospital_contact']
        hospital_address = request.form['hospital_address']

        hospital  = Hospital(
            hospital_name=hospital_name,
            hospital_company_name=hospital_company_name,
            hospital_email=hospital_email,
            hospital_contact=hospital_contact,
            hospital_address=hospital_address
        )
        db.session.add(hospital)
        db.session.commit()
        return redirect(url_for('hospital_view'))
    return render_template('hospital_create.html')


@app.route("/hospital_update/<int:id>", methods=["GET","POST"])
def hospital_update(id):
    hospital = Hospital.query.filter_by(id=id).first()
    if hospital:
        if request.method == "POST":
            hospital.hospital_name = request.form.get('hospital_name')
            hospital.hospital_company_name = request.form.get('hospital_company_name')
            hospital.hospital_email = request.form.get('hospital_email')
            hospital.hospital_contact = request.form.get('hospital_contact')
            hospital.hospital_address = request.form.get('hospital_address')

            db.session.commit()
            return redirect(url_for('hospital_view'))
    return render_template('hospital_edit.html', hospital=hospital)


@app.route('/hospital_view')
def hospital_view():
    allhospital = Hospital.query.all()
    hospital_count = Hospital.query.count()
    return render_template('hospital_view.html', hospital =allhospital, hospital_count=hospital_count)


@app.route("/delete/hospital/<int:id>")
def delete_hospital(id):
    hospital = Hospital.query.filter_by(id=id).first()
    if hospital:
        db.session.delete(hospital)
        db.session.commit()
    return redirect(url_for('hospital_view'))

@app.route('/user_view')
def user_view():
    return render_template('user_view.html')


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
