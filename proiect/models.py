from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(100), nullable=False)
    facultate = db.Column(db.String(100), nullable=False)
    medie = db.Column(db.Float, nullable=False)
    status_bursa = db.Column(db.String(50), default="In asteptare")

    def __repr__(self) -> str:
        return f"<Student {self.nume}>"
