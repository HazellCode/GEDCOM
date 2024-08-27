# 
# Author: Archie
# Date: 24/06/2022
# File Name: makeSimpleTree
# Description: 
#
# Imports
from parser import parseFamilyTree
from Tools.getParentsOfPerson import getParentsOfPerson
from Tools.getSlibingsOfIndividual import getSiblingsOfIndividuals
processedids = []
def makeSimpleTree(indi,PL,FL,count):

    if PL[indi].ID == "@I4586@":
        pass
    if indi == "":

        return {
            "error": "An Invalid ID Was Used",
            "reason": "No ID was provided"
        }
    if indi == "@":

        return {
            "error": "This is an invalid id",
            "reason": "Only an @ symbol was provided"
        }
    if indi[0] != "@":
        return {
            "error": "This is an invalid id.",
            "reason": "Does not start with an @ symbol"
        }
    try:
        parlist = getParentsOfPerson(indi,PL,FL)
    except:
        return {
            "error": "Couldn't get Parents of this Person",
            "reason": "This individual could not be found"

        }
    try:
        siblist = getSiblingsOfIndividuals(indi,PL,FL)
    except Exception as e:

        return {
            "error": "Couldn't get Siblings for this Personadsads",
            "reason": "This Individual couldn't be found",
            "detail": e,
        }

    count += 1
    if indi == '':
        return
    if siblist == None:
        siblist = []
    return {
            "id": PL[indi].ID,
            "name": PL[indi].NAME.PERSONAL_NAME_PIECES.GIVEN,
            "surname": PL[indi].NAME.PERSONAL_NAME_PIECES.SURNAME,
            "sex": (PL[indi].SEX.SEX if PL[indi].SEX.SEX else "None"),
            "born": PL[indi].BIRT.i_event_detail.event_detail.DATE,
            "generation": count,
            "ochil": [makeSimpleTree(sib, PL, FL, count) for sib in siblist],
            "parents": [makeSimpleTree(parent, PL, FL, count) for parent in parlist]
    }
