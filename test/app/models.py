from app import db
from datetime import datetime

class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    release_date = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(64), index=True, unique=True)
    director = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(200), nullable=True)
    budget = db.Column(db.Float, nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))

    def __repr__(self):
        return f"Name: {self.name} Genre: {self.genre} Release_date: {self.release_date} Director: {self.director} Description: {self.description} Budget: {self.budget}"

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(64), index=True, unique=True)
    films = db.relationship('Film', backref='genre', lazy='dynamic')

    def __repr__(self):
        return f'{self.genre}'