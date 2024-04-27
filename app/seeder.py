from models import db, Scan, Setting, Exploit, Parsed, Report, User

from pathlib import Path
from datetime import datetime
import json
import os
from werkzeug.security import generate_password_hash

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
    scans.append(Scan(scan_data=data, ip=ip, start_time=datetime.now(), end_time=datetime.now(), status='complete'))
    f.close()

with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.add_all(scans)
    db.session.commit()

print("Added " + str(count) + " files to database from " + directory)

user1 = User(
    username='test',
    password=generate_password_hash('test', "pbkdf2:sha256")
    )
with app.app_context():
    db.session.add(user1)
    db.session.commit()

directory = "./seed/reports"
count = 0
reports = []
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    f = open(os.path.join(directory, filename))
    data = f.read()
    ip = Path(os.path.join(directory, filename)).stem
    count += 1
    match_scan = False
    with app.app_context():
        scan = Scan.query.filter_by(ip=ip).first()
        if scan:
            reports.append(Report(content=data, ip=ip, time=datetime.now(), scan=scan))
            match_scan = True
            print(f"Report for {ip} has a matching scan")
    if not match_scan:
        reports.append(Report(content=data, ip=ip, time=datetime.now()))
    f.close()

with app.app_context():
    # db.drop_all()
    # db.create_all()
    db.session.add_all(reports)
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
    scans.append(Exploit(exploit_data=data, ip=ip, start_time=datetime.now(), end_time=datetime.now(), status='complete'))
    f.close()

with app.app_context():
    # db.drop_all()
    # db.create_all()
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
    scans.append(Parsed(parsed_data=data, ip=ip, start_time=datetime.now(), end_time=datetime.now(), status='complete'))
    f.close()

with app.app_context():
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