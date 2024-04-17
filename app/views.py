from flask import Blueprint, render_template, Markup, abort
import os
import markdown
from models import db, Report
import datetime

index = Blueprint('index', __name__, static_folder='static', template_folder='templates')


@index.route('/')
def home():
    return render_template('index.html')

@index.route('/scans')
def show_scans():
    return render_template('general_scans.html')

@index.route('/reports/<id>')
def show_report(id):
    """
    Renders a webpage that displays the report with the specified id.
    args:
        id: The id field of the report in the database
    """
    report = Report.query.filter_by(id=id).first()
    if not report:
        return abort(404)
    report_markdown = report.content
    report_html = markdown.markdown(report_markdown, extensions=['tables', "sane_lists"])
    report_html = report_html.replace("<table>", '<table class="table">')
    report_html = Markup(report_html)
    return render_template('report.html', report=report_html)

@index.route("/reports")
def list_reports():
    # Renders a webpage with a list of reports
    reports = Report.query.all()
    ret = []
    if reports:
            ret = [(report.id, report.ip, report.time.strftime("%Y-%M-%D"), report.time.strftime("%H:%M:%S")) for report in reports]
    message = ""
    if len(ret) == 0:
        message = "You have not done any scan"
    return render_template('report_list.html', report_names=ret, message=message)