import datetime

from flask import jsonify

from o_evmt.extensions import db
from .personne import Personne


class Exposant(Personne):
    __tablename__ = 'exposant'
    id = db.Column(db.Integer, db.ForeignKey("personne.id"), primary_key=True)
    domaine_id = db.Column(db.Integer, db.ForeignKey('domaine.id'))
    specialisation = db.Column(db.String(50), nullable=False)
    abonnement = db.Column(db.String(50), nullable=False)
    abonPub = db.Column(db.String(50), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "exposant"
    }

    def __init__(self, nom, prenom, dateNaiss, pays, ville, mail, telephone, specialisation, abonnement, abonPub, idDomaine):
        Personne.__init__(self, nom, prenom, dateNaiss, pays, ville, mail, telephone)
        self.specialisation = specialisation
        self.abonnement = abonnement
        self.abonPub = abonPub
        self.domaine_id = idDomaine

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def exists(id_exposant):
        return Exposant.query.get(id_exposant) is not None
    @staticmethod
    def getWithId(id_exposant):
        return Exposant.query.get(id_exposant)

    def format(self):
        return {
                'nom': self.nom,
                'prenom': self.prenom,
                'dateNaiss': self.dateNaiss,
                'pays': self.pays,
                'ville': self.ville,
                'mail': self.mail,
                'telephone': self.telephone,
                'domaine_id': self.domaine_id,
                'specialisation': self.specialisation,
                'abonnement': self.abonnement,
                'abonPub': self.abonPub
            }

