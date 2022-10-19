from o_evmt.extensions import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    exposant_id = db.Column(db.Integer, db.ForeignKey('exposant.id'))
    texte = db.Column(db.String(500), nullable=False)
    lienPhoto = db.Column(db.String(500), nullable=True)
    lienVideo = db.Column(db.String(500), nullable=True)

    def format(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "exposant_id": self.exposant_id,
            "texte": self.texte,
            "lienPhoto": self.lienPhoto,
            "lien_video": self.lienVideo
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
    def exists(id_message):
        return Message.query.get(id_message) is not None

    @staticmethod
    def has_right_access(id_message, id_client, id_exposant):
        if Message.exists(id_message):
            message = Message.query.get(id_message)
            return False if id_client != message.client_id and id_exposant != message.exposant_id else message
        return False
