# 
# Author: Archie
# Date: 23/06/2022
# File Name: main
# Description: 
#
# Imports
import logging

import flask
from flask import Flask, render_template, request, jsonify
from Tools.getFamilyMembers import getFamilyMembers
from Tools.getAllIndividuals import getAllIndividuals
from Tools.createAttributeList import createAttributeList
from Tools.getSlibingsOfIndividual import getSiblingsOfIndividuals_rFam
from Tools.getParentsOfPerson import getParentsOfPerson_rFam
from parserV2 import Parse
import time
import json
import uuid


logging.basicConfig(level=logging.ERROR)




PersonList = None
FamilyList = None
FileHead = None

# genlist = makeFamilyTree("@I262196792752@", PersonList, FamilyList,0)


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/file_stats")
def file_information():
    return render_template("file_information.html")

@app.route('/start')
def start():
    return render_template('start.html', PL=PersonList, FL=FamilyList)


@app.route('/tree', methods=['GET', 'POST'])
def horiz():
    return render_template('horizontal.html', tree=simpletree, PL=PersonList, FL=FamilyList)




@app.route('/profile', methods=['GET', 'POST'])
def inlinetree():
    if not PersonList or not FamilyList:
        return flask.redirect("/error")

    return render_template('profile.html', tree=simpletree, PL=PersonList, FL=FamilyList)


@app.route('/error', methods=['GET', 'POST'])
def error():
    return render_template('error.html', error={"error": "No Data", "reason": "No tree has been processed yet!"})


# API Shit
@app.route("/api/file_stats", methods=['GET','POST'])
def getFileStats():
    return {'data': FileHead}


@app.route("/api/getTreeInformation", methods=['GET', 'POST'])
def apiGetTreeInfo():
    if request.method == "POST":
        req = request.get_json()
        print("[api/getTreeInformation][POST] - " + str(req))

        global lastuuid
        global lastid
        global simpletree
        global uuid
        id = req['id']
        rec = req['uuid']

        # this is to increase efficieny. it check to see if the current id is the same as the last one requested
        # if it is then we dont need to recalculate the tree so we can just skip that and just return the pace again
        if id != lastid:
            lastuuid = None
        if rec != lastuuid:
            print("[api/getTreeInformation] - Building Tree")
            simpletree = None
            s_t = time.time()
            simpletree = createAttributeList(id, PersonList, FamilyList, 0)
            genuuid = uuid.uuid4()
            completedtime = "{:f}".format((time.time() - s_t))
            print("[api/getTreeInformation] tree generation took: " + str(completedtime) + "s")

            lastuuid = str(genuuid)
            lastid = id
            return jsonify({"data": simpletree, "uuid": genuuid, "ctime": completedtime})
        else:
            print("[api/getTreeInformation][POST]" + " - ID hasn't changed no need to regen tree")
            return jsonify({"data": "_304"})


@app.route("/api/getIndividuals", methods=['GET', 'POST'])
def apiGetIndividuals():
    if request.method == "POST":
        if not PersonList and not FamilyList:
            return {"status": "-1","data": "Error No File Has Been Uploaded"}
        allIndividuals = getAllIndividuals(PersonList)
        return jsonify({"data": allIndividuals})


@app.route("/api/getAllDataIndividual", methods=['GET', 'POST'])
def apiGetAllDataIndividual():
    if request.method == "POST":

        req = request.get_json()
        output = getAllIndividualData(req)

        # We also want to get the siblings of the individual
        return jsonify({"data": output})
    else:
        pass


@app.route("/api/getFamilyData", methods=['GET', 'POST'])
def apiGetFamilyData():
    if request.method == "POST":
        req = request.get_json()
        famlist = req["data"]
        print(famlist)
        try:
            input_opt = req["input_opt"]
        except:
            input_opt = False
        if not input_opt:
            pass
        else:
            output = {}
            if famlist == {}:
                return {"error": "This user has no children / partner"}
            for fam in famlist:
                print("fams")
                print(famlist[fam])
                output[fam] = {}
                members = getFamilyMembers(fam, FamilyList)
                print(members)
                if input_opt == "s":
                    for member in members[fam]['parents']:
                        relation = members[fam]['parents'][member][member]
                        members[fam]['parents'][member] = []
                        members[fam]['parents'][member] = getAllIndividualData(
                            {"id": [member], "input_opt": "ret_plain"})
                        members[fam]['parents'][member]['relation'] = relation
                    for member in members[fam]['children']:
                        members[fam]['children'][member] = []
                        members[fam]['children'][member] = getAllIndividualData(
                            {"id": [member], "input_opt": "ret_plain"})
                return jsonify(members)


@app.route("/api/getSiblings", methods=['GET', 'POST'])
def apiGetSiblings():
    if request.method == "POST":
        data = {}
        req = request.get_json()
        ids = req['ids']


@app.route("/api/userGED", methods=["GET","POST"])
def processUserGED():
    if request.method == "POST":
        req = request.get_json()
        global PersonList
        global FamilyList
        global FileHead
        newtree = Parse(req['data'])

        PersonList = newtree['People']
        FamilyList = newtree['Family']
        FileHead = newtree['HEAD']
        # Status Codes:
        #   0 = Success - Redirect User
        return {"status":0}


def debug(text):
    print(text)
    return ''


def getAllIndividualData(req):
    ids = req["id"]
    try:
        input_opt = req["input_opt"]
    except:
        input_opt = False
    if not input_opt:
        output = {}

        for id in ids:
            try:
                PersonList[id]['SIBLINGS']
                PersonList[id]['PARENTS']
            except:
                PersonList[id]['SIBLINGS'] = getSiblingsOfIndividuals_rFam(id, PersonList, FamilyList)
                PersonList[id]['PARENTS'] = getParentsOfPerson_rFam(id, PersonList, FamilyList)
            output[PersonList[id]['id']] = json.loads(
                json.dumps(PersonList[id], default=lambda o: o.__dict__, indent=4))
    else:
        if input_opt == "f":
            output = {}
            for fam in ids:
                output[fam] = {}
                print(ids)
                for obj in ids[fam]:
                    if not isinstance(obj,str):
                        id = list(obj.keys())[0]
                        relation = obj[id]
                    else:
                        id = obj

                    try:
                        PersonList[id]['SIBLINGS']
                        PersonList[id]['PARENTS']
                    except:
                        PersonList[id]['SIBLINGS'] = getSiblingsOfIndividuals_rFam(id, PersonList, FamilyList)
                        PersonList[id]['PARENTS'] = getParentsOfPerson_rFam(id, PersonList, FamilyList)
                    output[fam][PersonList[id]['id']] = json.loads(
                        json.dumps(PersonList[id], default=lambda o: o.__dict__, indent=4))
                    if not isinstance(obj, str):
                        output[fam][PersonList[id]['id']]['relation'] = relation
        elif input_opt == "ret_plain":
            output = {}
            for id in ids:
                try:
                    PersonList[id]['SIBLINGS']
                    PersonList[id]['PARENTS']
                except:
                    try:
                        PersonList[id]['SIBLINGS'] = getSiblingsOfIndividuals_rFam(id, PersonList, FamilyList)
                        PersonList[id]['PARENTS'] = getParentsOfPerson_rFam(id, PersonList, FamilyList)

                    except:
                        logging.error("[individual][error] " + str(id) + " doesn't exist")
                        output = {}
                        return output
                output = json.loads(json.dumps(PersonList[id], default=lambda o: o.__dict__, indent=4))

    return output


simpletree = ""
pass


lastuuid = None
lastid = None



if __name__ == '__main__':

    app.run()
