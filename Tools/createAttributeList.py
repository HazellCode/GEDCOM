# 
# Author: Archie
# Date: 09/07/2022
# File Name: createAttributeList
# Description: 
#
# Imports
from Tools.getParentsOfPerson import getParentsOfPerson
from Tools.getSlibingsOfIndividual import getSiblingsOfIndividuals
import logging

processedids = []
output = {}
logging.basicConfig(level=logging.ERROR)


def createAttributeList(indi, PL, FL, count):
    global output
    if isinstance(indi, dict):
        indi = list(indi.keys())[0]
    try:
        logging.debug("[individual]" + str(indi) + " - " + str(PL[indi]['NAME']['GIVN']))
        if indi == "@I262196741761@":
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

            logging.debug("[parents]")
            parlist = getParentsOfPerson(indi, PL, FL)
        except:
            return {
                "error": "Couldn't get Parents of this Person",
                "reason": "This individual could not be found",
                "detail": "The parents of : " + str(indi) + " could not be found"

            }
        try:
            logging.debug("[siblings]")
            siblist = getSiblingsOfIndividuals(indi, PL, FL)
        except Exception as e:
            logging.error("[siblings][error] - " + str(e))
            return {
                "error": "Couldn't get Siblings for this Personadsads",
                "reason": "This Individual couldn't be found"
            }

        if indi == '':
            return
        if siblist == None:
            siblist = []

        if indi not in processedids:
            # this massively improves the efficiency of the algorithm as it prevent processing the same person more than once
            # eg if someone has 7 siblings then each of the siblings will be processed 7 times
            # e.g 8 * 7 = 56 times instead of just processing each person once.
            # large tree's now load in under a second rather than taking multiple seconds to load (anywhere from 4 - 10 seconds)
            #

            output[indi] = {
                "id": PL[indi]['id'],
                "data": PL[indi],
                "generation": count,
                "ochil": siblist,
                "parents": parlist,
                "syscode": "_200"
            }

            processedids.append(indi)
            for sib in siblist:
                createAttributeList(sib, PL, FL, count)
            for par in parlist:
                createAttributeList(par, PL, FL, count + 1)
        return output
    except Exception as e:
        if str(e) != '':
            logging.error("[individual][error] - Individual has been referenced but doesn't exist" + str(e))
            output[str(e)] = {
                "id": str(e).strip("'"),
                "data": {
                    "NAME": {
                        "NAME": ["unknown"],
                        "SURN": ["unknown"]
                    },

                    "SEX": ['unkown'],
                    "BIRT": {
                        "DATE": ['unknown']
                    },
                },
                "generation": count,
                "ochil": [],
                "parents": [],
                "sysnote": "[individual][error] - Individual has been referenced but doesn't exist",
                "syscode": "_404"
            }
        else:
            logging.error("[individual][error] - Individual has been referenced by has no ID")
