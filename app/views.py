from flask import Blueprint, render_template, Markup
import os
import markdown

index = Blueprint('index', __name__, static_folder='static', template_folder='templates')


@index.route('/')
def home():
    return render_template('index.html')

@index.route('/scans')
def show_scans():
    return render_template('general_scans.html')

@index.route('/reports')
def show_report():
    cur_dir = os.path.dirname(__file__)
    test_path = os.path.join(cur_dir, "seed/reports/finalReport.md")
    test_file = open(test_path, "r")
    report_markdown = test_file.read()
    report_html = markdown.markdown(report_markdown, extensions=['tables'])
    report_html = Markup(report_html)
    report_html = report_html.replace("<table>", '<table class="table">')
    return render_template('report.html', report=report_html)