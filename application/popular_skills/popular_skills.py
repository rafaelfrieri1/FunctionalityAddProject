import requests
import numpy as np

from flask import Blueprint, request, make_response, jsonify
from flask import current_app as app

popular_skills_bp = Blueprint('popular_skills_bp', __name__)

@popular_skills_bp.route('/popular-skills', methods = ['GET'])
def popular_skills():
    if request.method != 'GET' :
        return make_response('Wrong query performed.', 400)

    paramsReq = {'offset':'0', 'size':'0', 'aggregate':'true'}
    resp = requests.post('https://search.torre.co/opportunities/_search', params = paramsReq)

    if resp.status_code == 400:
        return make_response('Information API is not responding.', 400)

    skills = resp.json()['aggregators']['skill']
    amount = np.array([])
    name = np.array([])

    for skill in skills:

        if len(amount) < 5:
            amount = np.append(amount, skill['total'])
            name = np.append(name, skill['value'])
        
        if (min(amount) < skill['total']) and (len(amount) == 5):
            minIndexRes = np.where(amount == min(amount))
            minIndex = minIndexRes[0]
            amount[minIndex[0]] = skill['total']
            name[minIndex[0]] = skill['value']
    sortIndexes = np.argsort(-amount, kind = 'mergesort')

    amountSent = np.array([])
    nameSent = np.array([])
    percentageSent = np.array([])
    totalJobOpportunities = resp.json()['total']

    for index in sortIndexes:
        amountSent = np.append(amountSent, amount[index])
        nameSent = np.append(nameSent, name[index])
        percentageSent = np.append(percentageSent, (amount[index]/totalJobOpportunities)*100)


    pop_skills = {'total': amountSent.tolist(), 'value': nameSent.tolist(), 'percentage_jobs': percentageSent.tolist()}
    headers = {'Content-Type': 'applicaton/json'}

    return make_response(jsonify(pop_skills), 200, headers)