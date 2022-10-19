from o_evmt.extensions import db


class Domaine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(50), nullable=False)

    def __init__(self, libelle):
        self.libelle = libelle

    def format(self):
        return {"id": self.id, "libelle": self.libelle}

    def insert(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def insertRange(domains):
        total = 0
        for domain in domains:
            if type(domain) is Domaine:
                db.session.add(domain)
                total += 1
        db.session.commit()
        return total
