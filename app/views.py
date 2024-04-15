from flask import Blueprint, render_template, Markup
import os
import markdown
from models import db, Report

index = Blueprint('index', __name__, static_folder='static', template_folder='templates')


@index.route('/')
def home():
    return render_template('index.html')

@index.route('/scans')
def show_scans():
    return render_template('general_scans.html')

@index.route('/reports/<id>')
def show_report(id):
    report_markdown = Report.query.filter_by(id=id).first()
    if not report_markdown:
        cur_dir = os.path.dirname(__file__)
        test_path = os.path.join(cur_dir, "seed/reports/finalReport.md")
        test_file = open(test_path, "r")
        report_markdown = test_file.read()
        report = Report(user=0, ip="10.10.0.14", content=report_markdown)
        db.session.add(report)
        db.session.commit()
        print("added")
    report_html = markdown.markdown(report_markdown, extensions=['tables', "sane_lists"])
    report_html = report_html.replace("<table>", '<table class="table">')
    report_html = Markup(report_html)
    return render_template('report.html', report=report_html)