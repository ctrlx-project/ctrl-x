from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Scans(db.Model):
    __tablename__ = 'scans'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(15), nullable=False)
    scan_data = db.Column(db.JSON, nullable=False)
