from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(60), primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(40), nullable=False)
    salary = db.Column(db.Integer, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    cname = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Users(email={self.email}, name={self.name}, surname={self.surname})>"

class Patients(db.Model):
    __tablename__ = 'patients'
    email = db.Column(db.String(60), db.ForeignKey('users.email'), primary_key=True)

    user = db.relationship('Users', backref='patient', lazy=True)

    def __repr__(self):
        return f"<Patients(email={self.email})>"

class Doctors(db.Model):
    __tablename__ = 'doctor'
    email = db.Column(db.String(60), db.ForeignKey('users.email'), primary_key=True)
    degree = db.Column(db.String(20), nullable=False)

    user = db.relationship('Users', backref='doctor', lazy=True)

    def __repr__(self):
        return f"<Doctors(email={self.email}, degree={self.degree})>"

class PublicServants(db.Model):
    __tablename__ = 'publicservant'
    email = db.Column(db.String(60), db.ForeignKey('users.email'), primary_key=True)
    department = db.Column(db.String(50), nullable=False)

    user = db.relationship('Users', backref='public_servant', lazy=True)

    def __repr__(self):
        return f"<PublicServants(email={self.email}, department={self.department})>"

class DiseaseType(db.Model):
    __tablename__ = 'diseasetype'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(140), nullable=False)

    def __repr__(self):
        return f"<DiseaseType(id={self.id}, description={self.description})>"

class Disease(db.Model):
    __tablename__ = 'disease'
    disease_code = db.Column(db.String(50), primary_key=True)
    pathogen = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(140), nullable=False)
    id = db.Column(db.Integer, db.ForeignKey('diseasetype.id'), nullable=False)

    disease_type = db.relationship('DiseaseType', backref='diseases', lazy=True)

    def __repr__(self):
        return f"<Disease(disease_code={self.disease_code}, pathogen={self.pathogen}, description={self.description}, disease_type={self.disease_type.description})>"
