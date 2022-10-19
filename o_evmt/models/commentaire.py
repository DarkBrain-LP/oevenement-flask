from .personne import db


class Commentaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('personne.id'))
    publication_id = db.Column(db.Integer, db.ForeignKey('publication.id'))
    texteCom = db.Column(db.String(500), nullable=False)
    lienPhoto = db.Column(db.String(255), nullable=False)

    def __init__(self, client, publication, commentaire, photo):
        self.client_id = client,
        self.publication_id = publication,
        self.texteCom = commentaire,
        self.lienPhoto = photo

    def commentaire_format(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'publication_id': self.publication_id,
            'texteCom': self.texteCom,
            'lienPhoto': self.lienPhoto
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()