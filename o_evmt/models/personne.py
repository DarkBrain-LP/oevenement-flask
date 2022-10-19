from o_evmt.extensions import db


class Personne(db.Model):
    __tablename__ = "personne"
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(20), nullable=False)
    prenom = db.Column(db.String(30), nullable=False)
    dateNaiss = db.Column(db.Date, nullable=False)
    pays = db.Column(db.String(30), nullable=False)
    ville = db.Column(db.String(20), nullable=False)
    mail = db.Column(db.String(50), nullable=False, unique=True)
    telephone = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(20), nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "personne",
        "polymorphic_on": type
    }

    def __init__(self, nom, prenom, dateNaiss, pays, ville, mail, telephone):
        self.nom = nom
        self.prenom = prenom
        self.dateNaiss = dateNaiss
        self.pays = pays
        self.ville = ville
        self.mail = mail
        self.telephone = telephone
