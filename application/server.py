import json
import logging

from flask import request, jsonify, make_response, Response
from sqlalchemy.exc import IntegrityError

from application import app, service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

@app.route("/")
def index():
    return 'OK'

@app.route('/cases', methods=['POST'])
def casework_post():
    try:
        service.save_case(request.get_json())
    except IntegrityError:
        print 'Failed to save'
        return 'Failed to save casework item.', 400
    except KeyError as e:
        logger.error(e.message)
        print 'Invalid data'
        return 'Invalid data', 400
    except Exception as e:
        print 'Unknown error.', e
        return 'Unknown error.', 400

    return 'Saved case', 200

@app.route('/cases', methods=['GET'])
def get_cases():
    return Response(json.dumps([i.serialize for i in service.get_case_items()]), mimetype='application/json')

@app.route('/cases/<title_number>', methods=(['PUT']))
def update_work_queue_for_case(title_number):
    try:
        if not service.update_case_with_work_queue(title_number, request.json):
            return 'Invalid data when updating the case for title: %s' % title_number, 400
    except KeyError as e:
        return 'Invalid data when updating the case for title: %s' % title_number, 400
    return 'OK', 200


@app.route('/cases/complete/<title_number>', methods=['PUT'])
def complete_case(title_number):
    if not service.update_case_with_status(title_number, new_status='complete'):
        return 'Update to case: %s was not successful' % title_number, 400
    return 'OK', 200



