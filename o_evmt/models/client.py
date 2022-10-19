from o_evmt.extensions import db
from .personne import Personne


class Client(Personne):
    __tablename__ = 'client'
    id = db.Column(db.Integer, db.ForeignKey("personne.id"), primary_key=True)
    profession = db.Column(db.String(30), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "client"
    }

    def __init__(self, nom, prenom, dateNaiss, pays, ville, mail, telephone, profession):
        Personne.__init__(self, nom, prenom, dateNaiss, pays, ville, mail, telephone)
        self.profession = profession

    def client_format(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'prenom': self.prenom,
            'dateNaiss': self.dateNaiss,
            'pays': self.pays,
            'ville': self.ville,
            'mail': self.mail,
            'telephone': self.telephone,
            'profession': self.profession
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def exists(id_entreprise):
        entreprise = Client.query.get(id_entreprise)
        return entreprise if entreprise is not None else False
