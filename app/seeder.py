from models import db, Scan, Setting
from pathlib import Path
import json
import os

from app import create_app

app = create_app()

directory = "./seed/nmap"

count = 0
scans = []
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    f = open(os.path.join(directory, filename))
    data = json.load(f)
    ip = Path(os.path.join(directory, filename)).stem
    count += 1
    scans.append(Scan(scan_data=data, ip=ip))
    f.close()

with app.app_context():
    db.create_all()
    db.session.add_all(scans)
    db.session.commit()

print("Added " + str(count) + " files to database")

with open('seed/settings.json', 'r') as file:
    settings_sample_data = json.load(file)

settings = []
for pref in settings_sample_data:
    setting = Setting(key=pref['key'], value=pref['value'])
    settings.append(setting)

with app.app_context():
    db.session.add_all(settings)
    db.session.commit()
