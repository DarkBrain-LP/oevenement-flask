from o_evmt.extensions import db
from o_evmt.models.domaine import Domaine


class Entreprise(db.Model):
    __tablename__ = 'entreprises'

    id = db.Column(db.Integer, primary_key=True)
    nomEntreprise = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.String(100), nullable=False)
    pays = db.Column(db.String(30), nullable=False)
    ville = db.Column(db.String(20), nullable=False)
    mail = db.Column(db.String(50), nullable=False, unique=True)
    contact = db.Column(db.Integer, nullable=False)

    domaine_id = db.Column(db.Integer, db.ForeignKey('domaine.id'))
    abonnement = db.Column(db.String(50), nullable=False)
    abonPub = db.Column(db.String(50), nullable=False)

    def __init__(self, nom, description, pays, ville, mail, contact, domaine_id, abonnement, abonPub):
        self.nomEntreprise = nom
        self.description = description
        self.pays = pays
        self.ville = ville
        self.mail = mail
        self.contact = contact
        self.domaine_id = domaine_id
        self.abonnement = abonnement
        self.abonPub = abonPub

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
        entreprise = Entreprise.query.get(id_entreprise)
        return entreprise if entreprise is not None else False

    @staticmethod
    def getWithId(id_entreprise):
        return Entreprise.query.get(id_entreprise)

    def format(self):
        return {
            'id': self.id,
            'nom': self.nomEntreprise,
            'description': self.description,
            'pays': self.pays,
            'ville': self.ville,
            'mail': self.mail,
            'contact': self.contact,
            'domaine': Domaine.query.get(self.domaine_id).format(),
            'abonnement': self.abonnement,
            'abonPub': self.abonPub
        }

# db.create_all(app=create_app())
# TODO : Create/generate the table 'entreprises'
