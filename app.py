from flask import Flask, render_template, request, redirect, url_for
from models import Disease, DiseaseType, Doctors, Patients, PublicServants, db, Users
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return redirect(url_for('list_users'))

# CRUD: Create a User
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        surname = request.form['surname']
        salary = request.form['salary']
        phone = request.form['phone']
        cname = request.form['cname']

        new_user = Users(
            email=email, name=name, surname=surname, salary=salary, phone=phone, cname=cname
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('list_users'))

    return render_template('add_user.html')

# CRUD: Read/List Users
@app.route('/users')
def list_users():
    users = Users.query.all()
    return render_template('list_users.html', users=users)

# CRUD: Update a User
@app.route('/edit_user/<email>', methods=['GET', 'POST'])
def edit_user(email):
    user = Users.query.get(email)
    if request.method == 'POST':
        user.name = request.form['name']
        user.surname = request.form['surname']
        user.salary = request.form['salary']
        user.phone = request.form['phone']
        user.cname = request.form['cname']
        db.session.commit()
        return redirect(url_for('list_users'))

    return render_template('edit_user.html', user=user)

# CRUD: Delete a User
@app.route('/delete_user/<email>', methods=['POST'])
def delete_user(email):
    user = Users.query.get(email)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('list_users'))

if __name__ == '__main__':
    app.run(debug=True)

# CRUD: List Patients
@app.route('/patients')
def list_patients():
    patients = Patients.query.join(Users, Patients.email == Users.email).all()
    return render_template('list_patients.html', patients=patients)

# CRUD: Add a Patient
@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        email = request.form['email']

        # Check if the email exists in Users
        user = Users.query.get(email)
        if not user:
            return "Error: User with this email does not exist."

        # Check if the email is already a Patient
        if Patients.query.get(email):
            return "Error: This user is already a patient."

        new_patient = Patients(email=email)
        db.session.add(new_patient)
        db.session.commit()
        return redirect(url_for('list_patients'))

    users = Users.query.all()
    return render_template('add_patient.html', users=users)

# CRUD: Delete a Patient
@app.route('/delete_patient/<email>', methods=['POST'])
def delete_patient(email):
    patient = Patients.query.get(email)
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for('list_patients'))


# CRUD: List Doctors
@app.route('/doctors')
def list_doctors():
    doctors = Doctors.query.join(Users, Doctors.email == Users.email).all()
    return render_template('list_doctors.html', doctors=doctors)

# CRUD: Add a Doctor
@app.route('/add_doctor', methods=['GET', 'POST'])
def add_doctor():
    if request.method == 'POST':
        email = request.form['email']
        degree = request.form['degree']

        # Check if the email exists in Users
        user = Users.query.get(email)
        if not user:
            return "Error: User with this email does not exist."

        # Check if the email is already a Doctor
        if Doctors.query.get(email):
            return "Error: This user is already a doctor."

        new_doctor = Doctors(email=email, degree=degree)
        db.session.add(new_doctor)
        db.session.commit()
        return redirect(url_for('list_doctors'))

    users = Users.query.all()
    return render_template('add_doctor.html', users=users)

# CRUD: Delete a Doctor
@app.route('/delete_doctor/<email>', methods=['POST'])
def delete_doctor(email):
    doctor = Doctors.query.get(email)
    db.session.delete(doctor)
    db.session.commit()
    return redirect(url_for('list_doctors'))

# CRUD: List Public Servants
@app.route('/public_servants')
def list_public_servants():
    public_servants = PublicServants.query.join(Users, PublicServants.email == Users.email).all()
    return render_template('list_public_servants.html', public_servants=public_servants)

# CRUD: Add a Public Servant
@app.route('/add_public_servant', methods=['GET', 'POST'])
def add_public_servant():
    if request.method == 'POST':
        email = request.form['email']
        department = request.form['department']

        # Check if the email exists in Users
        user = Users.query.get(email)
        if not user:
            return "Error: User with this email does not exist."

        # Check if the email is already a Public Servant
        if PublicServants.query.get(email):
            return "Error: This user is already a public servant."

        new_public_servant = PublicServants(email=email, department=department)
        db.session.add(new_public_servant)
        db.session.commit()
        return redirect(url_for('list_public_servants'))

    users = Users.query.all()
    return render_template('add_public_servant.html', users=users)

# CRUD: Delete a Public Servant
@app.route('/delete_public_servant/<email>', methods=['POST'])
def delete_public_servant(email):
    public_servant = PublicServants.query.get(email)
    db.session.delete(public_servant)
    db.session.commit()
    return redirect(url_for('list_public_servants'))

# CRUD: List Disease Types
@app.route('/disease_types')
def list_disease_types():
    disease_types = DiseaseType.query.all()
    return render_template('list_disease_types.html', disease_types=disease_types)

# CRUD: Add a Disease Type
@app.route('/add_disease_type', methods=['GET', 'POST'])
def add_disease_type():
    if request.method == 'POST':
        id = request.form['id']
        description = request.form['description']

        # Check if the ID already exists
        if DiseaseType.query.get(id):
            return "Error: A disease type with this ID already exists."

        new_disease_type = DiseaseType(id=id, description=description)
        db.session.add(new_disease_type)
        db.session.commit()
        return redirect(url_for('list_disease_types'))

    return render_template('add_disease_type.html')

# CRUD: Update a Disease Type
@app.route('/edit_disease_type/<int:id>', methods=['GET', 'POST'])
def edit_disease_type(id):
    disease_type = DiseaseType.query.get(id)
    if request.method == 'POST':
        disease_type.description = request.form['description']
        db.session.commit()
        return redirect(url_for('list_disease_types'))

    return render_template('edit_disease_type.html', disease_type=disease_type)

# CRUD: Delete a Disease Type
@app.route('/delete_disease_type/<int:id>', methods=['POST'])
def delete_disease_type(id):
    disease_type = DiseaseType.query.get(id)
    db.session.delete(disease_type)
    db.session.commit()
    return redirect(url_for('list_disease_types'))

# CRUD: List Diseases
@app.route('/diseases')
def list_diseases():
    diseases = Disease.query.join(DiseaseType, Disease.id == DiseaseType.id).all()
    return render_template('list_diseases.html', diseases=diseases)

# CRUD: Add a Disease
@app.route('/add_disease', methods=['GET', 'POST'])
def add_disease():
    if request.method == 'POST':
        disease_code = request.form['disease_code']
        pathogen = request.form['pathogen']
        description = request.form['description']
        disease_type_id = request.form['disease_type_id']

        # Check if disease code already exists
        if Disease.query.get(disease_code):
            return "Error: A disease with this code already exists."

        # Check if the disease type exists
        disease_type = DiseaseType.query.get(disease_type_id)
        if not disease_type:
            return "Error: Invalid Disease Type."

        new_disease = Disease(disease_code=disease_code, pathogen=pathogen, description=description, id=disease_type_id)
        db.session.add(new_disease)
        db.session.commit()
        return redirect(url_for('list_diseases'))

    disease_types = DiseaseType.query.all()
    return render_template('add_disease.html', disease_types=disease_types)

# CRUD: Update a Disease
@app.route('/edit_disease/<string:disease_code>', methods=['GET', 'POST'])
def edit_disease(disease_code):
    disease = Disease.query.get(disease_code)
    if request.method == 'POST':
        disease.pathogen = request.form['pathogen']
        disease.description = request.form['description']
        disease.id = request.form['disease_type_id']
        db.session.commit()
        return redirect(url_for('list_diseases'))

    disease_types = DiseaseType.query.all()
    return render_template('edit_disease.html', disease=disease, disease_types=disease_types)

# CRUD: Delete a Disease
@app.route('/delete_disease/<string:disease_code>', methods=['POST'])
def delete_disease(disease_code):
    disease = Disease.query.get(disease_code)
    db.session.delete(disease)
    db.session.commit()
    return redirect(url_for('list_diseases'))


