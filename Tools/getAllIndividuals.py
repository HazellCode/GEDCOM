# 
# Author: Archie
# Date: 28/06/2022
# File Name: getAllIndividuals
# Description: Gets every individual from the tree and returns the name and id in a json format.
#
# Imports

def getAllIndividuals(PL):
    out = []

    for indi in PL:
        if indi == '@I110@':
            pass
        try:
            name = PL[indi]["NAME"]['GIVN']
        except:
            name = ["Unknown"]
        try:
            surname = PL[indi]["NAME"]['SURN']
        except:
            surname = ["Unknown"]
        try:
            birthdate = PL[indi]['BIRT']['DATE']
        except:
            birthdate = ["Unknown"]
        out.append({
            "id": indi,
            "name": name,
            "surname": surname,
            "born": birthdate
        })
    return out