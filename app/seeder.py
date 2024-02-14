from app import create_app
from models import db, Scans
from flask_sqlalchemy import SQLAlchemy
from scan import app
import json

from utils import pretty_print
from pathlib import Path

import os

directory = "./seed/nmap"

count = 0
scans = []
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    f = open(os.path.join(directory, filename))
    data = json.load(f)
    ip = Path(os.path.join(directory, filename)).stem
    count += 1
    scans.append(Scans(scan_data=data, ip=ip))
    f.close()

with app.app_context():
        db.create_all()
        db.session.add_all(scans)
        db.session.commit()

print("Added " + str(count) + " files to database")