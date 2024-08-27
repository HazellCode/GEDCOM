#
# Author: Archie
# Date: 21/07/2022
# File Name: main
# Description:
#

# Imports
import logging


def getFamilyMembers(family,FamilyList):
    output = {}
    output[family] = {}
    output[family]['parents'] = {}
    try:
        if FamilyList[family]['HUSB']:
            for husb in FamilyList[family]['HUSB']:

                output[family]['parents'][list(husb.keys())[0]] = husb
    except:
        logging.warning("[getFamilyMembers][warning] No Husband(s) found in this family ")
    try:
        if FamilyList[family]['WIFE']:
            for wife in FamilyList[family]['WIFE']:
                output[family]['parents'][list(wife.keys())[0]] = wife
    except:
        logging.warning("[getFamilyMembers][warning] No Wife/Wives found in this family ")
    output[family]['children'] = {}
    for child in FamilyList[family]['CHIL']:
        output[family]['children'][[child][0]] = []
        output[family]['children'][[child][0]] = child

    return output