from o_evmt.extensions import db

class Annonce(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    entreprise_id = db.Column(db.Integer, db.ForeignKey('entreprises.id'))
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'))
    coordonnees = db.Column(db.String(50), nullable=False)
    lienPhoto = db.Column(db.String(50))
    lienVideo = db.Column(db.String(50))