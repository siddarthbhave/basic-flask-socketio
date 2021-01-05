from app import db

class History(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    message = db.Column('message', db.String(550))

    def __repr__(self):
        return '<Message {}>'.format(self.message)
