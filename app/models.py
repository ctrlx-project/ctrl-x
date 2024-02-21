from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Scan(db.Model):
    __tablename__ = 'scans'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(15), nullable=False)
    scan_data = db.Column(db.JSON, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    end_time = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    job = db.relationship('ScanJob', backref='scan', uselist=False)


class ScanJob(db.Model):
    __tablename__ = 'scan_jobs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(15), nullable=False)
    start_time = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    end_time = db.Column(db.DateTime(timezone=True))
    status = db.Column(db.String(15))
    scan_id = db.Column(db.Integer, db.ForeignKey('scans.id', ondelete='CASCADE', onupdate='CASCADE'))

    @property
    def info(self):
        return {
            'id': self.id,
            'ip': self.ip,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'status': self.status,
            'scan_id': self.scan_id
        }
