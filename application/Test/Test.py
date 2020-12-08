from flask import Blueprint
from flask import current_app as app

test_bp = Blueprint('test_bp', __name__)

@test_bp.route('/test', methods = ['GET'])

def test():
    return "Hello World!"