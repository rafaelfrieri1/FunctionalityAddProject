import requests
import numpy as np

from flask import Blueprint, request, make_response, jsonify
from flask import current_app as app
from random import seed, randint

strength_based_search_bp = Blueprint('strength_based_search_bp', __name__)

def employeeSearch(employees, topEmployees, topUsernames, topScores, imageURLs, requiredStrengths, n):
    for employee in employees:
        if len(topEmployees) < n :
            topEmployees = np.append(topEmployees, employee["name"])
            topUsernames = np.append(topUsernames, employee["username"])
            topScores = np.append(topScores, score(employee, requiredStrengths))
            imageURLs = np.append(imageURLs, employee["picture"])
        
        if (len(topEmployees)) == n and score(employee, requiredStrengths)>min(topScores):
            minIndexRes = np.where(topScores == min(topScores))
            minIndex = minIndexRes[0]
            topEmployees[minIndex[0]] = employee["name"]
            topUsernames[minIndex[0]] = employee["username"]
            topScores[minIndex[0]] = score(employee, requiredStrengths)
            imageURLs[minIndex[0]] = employee["picture"]

    return [topEmployees, topUsernames, topScores, imageURLs]


def score(employee, requiredStrengths):
    empSkills = employee["skills"]
    scoreResult = 0
    for skill in empSkills:
        for strength in requiredStrengths:
            if skill["name"] == strength["name"] :
                scoreResult = scoreResult + skill["weight"] + 1
                break
    return scoreResult

@strength_based_search_bp.route('/strength-based-search/', methods = ['GET'])
def strength_based_search():
    if request.method != 'GET' :
        return make_response('Wrong query performed.', 400)

    jobID = request.args.get('job-id')
    n = int(request.args.get('size'))
    respOp = requests.get(f'https://torre.co/api/opportunities/{jobID}')
    if respOp.status_code != 200:
        return make_response('Information API of job opportunity with id is not responding.', 400)

    requiredStrengths = respOp.json()['strengths']
    first = True
    seed()
    randInitialize = randint(0, 400001)
    offset = randInitialize
    employees = []
    topEmployees = np.array([])
    topUsernames = np.array([])
    topScores = np.array([])
    imageURLs = np.array([])

    while ((len(employees) == 5000) or (first == True)) and offset != (randInitialize+10000):
        respEmployees = requests.post(f'https://search.torre.co/people/_search/?offset={offset}&size=5000&aggregate=false')
        if respEmployees.status_code == 400:
            return make_response('Information API of people search is not responding.', 400)
        
        employees = respEmployees.json()['results']
        resEmpSearch = employeeSearch(employees, topEmployees, topUsernames, topScores, imageURLs, requiredStrengths, n)
        topEmployees = resEmpSearch[0]
        topUsernames = resEmpSearch[1]
        topScores = resEmpSearch[2]
        imageURLs = resEmpSearch[3]

        if first == True:
            first = False

        offset = offset + 5000

    sortIndexes = np.argsort(-topScores, kind = 'mergesort')

    employeeSent = np.array([])
    userSent = np.array([])
    scoreSent = np.array([])
    urlsSent = np.array([])

    for index in sortIndexes:
        employeeSent = np.append(employeeSent, topEmployees[index])
        userSent = np.append(userSent, topUsernames[index])
        scoreSent = np.append(scoreSent, topScores[index])
        urlsSent = np.append(urlsSent, imageURLs[index])

    best_employees = {'names': employeeSent.tolist(), 'usernames':userSent.tolist(), 'scores': scoreSent.tolist(), 'pictures': urlsSent.tolist(), 'jobName': respOp.json()['serpTags']['title']}
    headers = {'Content-Type': 'applicaton/json'}

    return make_response(jsonify(best_employees), 200, headers)