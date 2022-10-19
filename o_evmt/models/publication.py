from o_evmt.extensions import db
from o_evmt.models.enterprise import Entreprise
from o_evmt.models.exposant import Exposant


class Publication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exposant_id = db.Column(db.Integer, db.ForeignKey('personne.id'))
    coordonnees = db.Column(db.String(50), nullable=False)
    lienPhoto = db.Column(db.String(50))
    lienVideo = db.Column(db.String(50))

    def __init__(self, exposant_id, coordonnees, lienPhoto, lienVideo):
        self.exposant_id = exposant_id
        self.coordonnees = coordonnees
        self.lienPhoto = lienPhoto
        self.lienVideo = lienVideo

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        creator = Exposant.query.get(self.exposant_id)
        if creator is None:
            creator = Entreprise.query.get(self.exposant_id)
        if creator is not None:
            return {
                "exposant": creator.format(),
                "coordonnees": self.coordonnees,
                "lienPhoto" : self.lienPhoto,
                "lienVideo" : self.lienVideo
            }
        return {
            "error": "Post creator not found"
        }
