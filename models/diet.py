from database import db

class Diet(db.Model):
    # id (int), Name (str), description str(80), date(date time), diet(Boolean)
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=db.func.now())
    snack = db.Column(db.Boolean, nullable=False, default=True)