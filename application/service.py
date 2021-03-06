import json
import logging

from application import db
from application.model import Case


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


def save_case(data):
    logger.info("Received POST new case. %s" % data)
    case = Case()
    case.title_number = data.get('title_number')
    case.application_type = data.get('application_type')
    case.request_details = json.dumps(data.get('request_details'))
    case.status = 'pending'
    q = data.get('work_queue', None)
    if q:
        case.work_queue = q
    case.submitted_by = data.get('submitted_by')

    db.session.add(case)
    db.session.commit()
    return case


def get_case_items():
    return Case.query.order_by(Case.submitted_at).all()

def get_cases_by_status_and_queue(status, work_queue):
    return Case.query.filter(Case.status.in_(['error', status])).filter(Case.work_queue == work_queue).order_by(Case.submitted_at).all()

def get_cases_by_title(title_number):
    return Case.query.filter(Case.title_number == title_number).order_by(Case.submitted_at).all()

def update_case_with_work_queue(case_id, data):
    logger.info("Received update for case %s, set work_queue to %s" % (case_id, data))
    q = data.get('work_queue', None)
    if not q:
        return False

    Case.query.filter_by(id=case_id).update(dict(work_queue=q))
    db.session.commit()
    return True

def update_case_with_status(case_id, new_status):
    logger.info("Received update for case: %s, set status to %s" % (case_id, new_status))
    if new_status not in ['pending', 'queued', 'approved', 'completed', 'wait', 'error']:
        logger.error('[%s] is an invalid choice for status of a case' % new_status)
        return False

    Case.query.filter_by(id=case_id).update(dict(status=new_status))
    db.session.commit()
    return True

def update_case_with_dict(case_id, data):
    logger.info("Received update for case %s, update with %s" % (case_id, data))

    Case.query.filter_by(id=case_id).update(data)
    db.session.commit()
    return True

def get_next_pending_case():
    return Case.query.filter_by(status='pending').order_by(Case.submitted_at).first()

def get_next_approved_case():
    return Case.query.filter_by(status='approved').order_by(Case.submitted_at).first()

def get_case(case_id):
    return Case.query.filter_by(id=case_id).first()
