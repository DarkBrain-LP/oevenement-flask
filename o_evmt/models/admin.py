from o_evmt.extensions import db

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(50), nullable=False, unique=True)
    # password =