from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Scan(db.Model):
    __tablename__ = 'scans'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(16), nullable=False)
    scan_data = db.Column(db.JSON, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(15))

    @property
    def info(self):
        return {
            'id':self.id,
            'ip':self.ip,
            'scan_data':self.scan_data,
            'start_time':self.start_time,
            'end_time':self.end_time,
            'status':self.status,
        }

class RawMeta(db.Model):
    __tablename__ = 'raw-meta'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(16), nullable=False)
    scan_data = db.Column(db.JSON, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(15))

class ParsedMeta(db.Model):
    __tablename__ = 'parsed-meta'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(16), nullable=False)
    scan_data = db.Column(db.JSON, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(15))


class Setting(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String(255), nullable=False)
    value = db.Column(db.Text)

    @property
    def info(self):
        return {
            'id': self.id,
            'key': self.key,
            'value': self.value
        }