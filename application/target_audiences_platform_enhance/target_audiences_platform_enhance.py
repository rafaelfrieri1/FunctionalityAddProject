import requests
import numpy as np

from flask import Blueprint, request, make_response, jsonify
from flask import current_app as app

target_audiences_platform_enhance_bp = Blueprint('target_audiences_platform_enhance_bp', __name__)

@target_audiences_platform_enhance_bp.route('/target-audiences-platform-enhance/', methods = ['GET'])
def target_audiences_platform_enhance():
    if request.method != 'GET' :
        return make_response('Wrong query performed.', 400)

    paramsReq = {'offset':'0', 'size':'0', 'aggregate':'true'}
    resp = requests.post(' https://search.torre.co/people/_search', params = paramsReq)

    if resp.status_code == 400:
        return make_response('Information API of job search is not responding.', 400)

    n = int(request.args.get('size'))
    skills = resp.json()['aggregators']['skill']
    amount = np.array([])
    name = np.array([])

    for skill in skills:

        if len(amount) < n:
            amount = np.append(amount, skill['total'])
            name = np.append(name, skill['value'])
        
        if (max(amount) > skill['total']) and (len(amount) == n):
            maxIndexRes = np.where(amount == max(amount))
            maxIndex = maxIndexRes[0]
            amount[maxIndex[0]] = skill['total']
            name[maxIndex[0]] = skill['value']

    sortIndexes = np.argsort(amount, kind = 'mergesort')

    amountSent = np.array([])
    nameSent = np.array([])
    percentageSent = np.array([])
    totalAmountOfPeople = resp.json()['total']

    for index in sortIndexes:
        amountSent = np.append(amountSent, amount[index])
        nameSent = np.append(nameSent, name[index])
        percentageIndex = (amount[index]/totalAmountOfPeople)*100
        percentageSent = np.append(percentageSent, round(percentageIndex, 3))


    unpopular_audience = {'total': amountSent.tolist(), 'value': nameSent.tolist(), 'percentage_jobs': percentageSent.tolist()}
    headers = {'Content-Type': 'applicaton/json', 'Access-Control-Allow-Origin':'https://torre-application-front.herokuapp.com'}

    return make_response(jsonify(unpopular_audience), 200, headers)