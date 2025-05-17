from db import db      # Con db importamos SQLAlchemy para que ande la tabla
from datetime import date

# Definir el modelo de eventos
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)

    # Funcion que devuelve en dias, la fecha de hoy
    def days_remaining(self):
        return (self.date - date.today()).days