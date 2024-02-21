from flask import Blueprint
from models import db, Scan, ScanJob
from utils import success_resp, error_resp

api = Blueprint('api', __name__, static_folder='static', template_folder='templates')


@api.route('/')
def _api():
    return success_resp("API is running")

