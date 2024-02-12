from app import create_app
from models import db, Scans
from flask_sqlalchemy import SQLAlchemy
from scan import app
import json

from utils import pretty_print
from pathlib import Path

import os

cwd = os.getcwd()
directory = cwd + "/seed"
    
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".json"): 
        # print(os.path.join(directory, filename))
        f = open(os.path.join(directory, filename))
        data = json.load(f)
        ip = Path(os.path.join(directory, filename)).stem
        print(os.path.join(directory, filename))
        with app.app_context():
            db.create_all()
            db.session.add(Scans(scan_data=data, ip=ip))
            db.session.commit()
        continue
    else:
        continue

