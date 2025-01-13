from flask_migrate import Migrate
from flask import Flask, flash, render_template, request, redirect, url_for
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

  
@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')


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
        return redirect(url_for('patient_view'))
    return render_template('patient_create.html')


@app.route('/patient_view')
def patient_view():
    allnew_patient = Patient.query.all()
    return render_template('patient_view.html', new_patient=allnew_patient)


@app.route("/hospital_create", methods=['GET', 'POST'])
def hospital_create():    
    if request.method == "POST":
        hospital_name = request.form['hospital_name']
        hospital_company_name = request.form['hospital_company_name']
        hospital_email = request.form['hospital_email']
        hospital_contact = request.form['hospital_contact']
        hospital_address = request.form['hospital_address']

        new_hospital = Hospital(
            hospital_name=hospital_name,
            hospital_company_name=hospital_company_name,
            hospital_email=hospital_email,
            hospital_contact=hospital_contact,
            hospital_address=hospital_address
        )
        db.session.add(new_hospital)
        db.session.commit()
        return redirect(url_for('hospital_view'))
    return render_template('hospital_create.html')


@app.route('/hospital_view')
def hospital_view():
    allnew_hospital = Hospital.query.all()
    return render_template('hospital_view.html', new_hospital=allnew_hospital)


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


@app.route("/delete/patient/<int:patient_id>")
def delete_patient(patient_id):
    patient = Patient.query.filter_by(patient_id=patient_id).first()
    if patient:
        db.session.delete(patient)
        db.session.commit()
    return redirect(url_for('patient_view'))

@app.route("/delete/hospital/<int:id>")
def delete_hospital(id):
    hospital = Hospital.query.filter_by(id=id).first()
    if hospital:
        db.session.delete(hospital)
        db.session.commit()
    return redirect(url_for('hospital_view'))

if __name__ == "__main__":
    app.run(debug=True)
