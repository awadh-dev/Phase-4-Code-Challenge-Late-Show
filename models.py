from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Episode(db.Model):
    __tablename__ = 'episodes'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    number = db.Column(db.Integer)
    appearances = db.relationship("Appearance", backref="episode", cascade="all, delete")

    def to_dict(self, include_appearances=False):
        data = {
            "id": self.id,
            "date": self.date,
            "number": self.number
        }
        if include_appearances:
            data["appearances"] = [a.to_dict(include_guest=True) for a in self.appearances]
        return data

class Guest(db.Model):
    __tablename__ = 'guests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    occupation = db.Column(db.String)
    appearances = db.relationship("Appearance", backref="guest", cascade="all, delete")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "occupation": self.occupation
        }

class Appearance(db.Model):
    __tablename__ = 'appearances'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'))
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'))

    def to_dict(self, include_guest=False, include_nested=False):
        data = {
            "id": self.id,
            "rating": self.rating,
            "guest_id": self.guest_id,
            "episode_id": self.episode_id
        }
        if include_guest:
            data["guest"] = self.guest.to_dict()
        if include_nested:
            data["guest"] = self.guest.to_dict()
            data["episode"] = self.episode.to_dict()
        return data
