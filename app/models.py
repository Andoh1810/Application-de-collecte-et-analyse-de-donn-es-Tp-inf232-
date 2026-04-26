from . import db

class Reponse(db.Model):
    __tablename__ = 'reponses'

    id = db.Column(db.Integer, primary_key = True)
    genre = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    filiere = db.Column(db.String(100), nullable=False)
    annee = db.Column(db.String(20), nullable=False)
    niveau_stress = db.Column(db.Integer, nullable=False)
    cause_stress = db.Column(db.String(50), nullable=False)
    heures_sommeil = db.Column(db.String(20), nullable=False)
    fait_sport = db.Column(db.String(10), nullable=False)
    songe_abandon = db.Column(db.String(5), nullable=False)
    gestion_stress = db.Column(db.String(50), nullable=False)