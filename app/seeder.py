from models import db, Scan, Setting, RawMeta, ParsedMeta, Report
from pathlib import Path
from datetime import datetime
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
    scans.append(Scan(scan_data=data, ip=ip+'/24', start_time=datetime.now(), end_time=datetime.now(), status='complete'))
    f.close()

with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.add_all(scans)
    db.session.commit()

print("Added " + str(count) + " files to database from " + directory)

directory = "./seed/exploit"

count = 0
scans = []
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    f = open(os.path.join(directory, filename))
    data = json.load(f)
    ip = Path(os.path.join(directory, filename)).stem
    count += 1
    scans.append(RawMeta(scan_data=data, ip=ip+'/24', start_time=datetime.now(), end_time=datetime.now(), status='complete'))
    f.close()

with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.add_all(scans)
    db.session.commit()

print("Added " + str(count) + " files to database from " + directory)

directory = "./seed/reports"
count = 0
scans = []
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    f = open(os.path.join(directory, filename))
    data = f.read()
    ip = Path(os.path.join(directory, filename)).stem
    count += 1
    scans.append(Report(content=data, ip=ip+'/24', time=datetime.now(), user=0))
    f.close()

with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.add_all(scans)
    db.session.commit()

print("Added " + str(count) + " files to database from " + directory)

directory = "./seed/scan_parser"

count = 0
scans = []
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    f = open(os.path.join(directory, filename))
    data = json.load(f)
    ip = Path(os.path.join(directory, filename)).stem
    count += 1
    scans.append(ParsedMeta(scan_data=data, ip=ip+'/24', start_time=datetime.now(), end_time=datetime.now(), status='complete'))
    f.close()

with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.add_all(scans)
    db.session.commit()

print("Added " + str(count) + " files to database from " + directory)

with open('seed/settings.json', 'r') as file:
    settings_sample_data = json.load(file)

settings = []
for pref in settings_sample_data:
    setting = Setting(key=pref['key'], value=pref['value'])
    settings.append(setting)

with app.app_context():
    db.session.add_all(settings)
    db.session.commit()
