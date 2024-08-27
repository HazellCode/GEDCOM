# 
# Author: Archie
# Date: 24/06/2022
# File Name: getParentsOfPerson
# Description: 
#
# Imports
import logging
logging.basicConfig(level=logging.ERROR)

def getParentsOfPerson(indi,PL,FL):
    famlist = []
    try:
        for fam in PL[indi]['FAMC']:
            for key in FL[fam]:
                if key == "HUSB" or key == "WIFE":
                    # We can get the parents of the family regardless of if there are two Husbands / Wives / a Wife and a Husband
                    if key == "HUSB":
                        # We have a husband
                        for husb in FL[fam][key]:
                            famlist.append(husb)

                    elif key == "WIFE":
                        # We have a husband
                        for wife in FL[fam][key]:
                            famlist.append(wife)
    except Exception as e:
        logging.error("[api/getTreeInformation][parents][error] No recorded Child -> Family Connection")
        logging.error("[api/getTreeInformation][parents][error] " + str(e))
    return famlist

def getParentsOfPerson_rFam(indi,PL,FL):
    famlist = {}
    try:

        for fam in PL[indi]['FAMC']:
            famlist[fam] = []
            print(FL[fam])
            for key in FL[fam]:
                if key == "HUSB" or key == "WIFE":
                    # We can get the parents of the family regardless of if there are two Husbands / Wives / a Wife and a Husband
                    if key == "HUSB":
                        # We have a husband
                        for husb in FL[fam][key]:
                            famlist[fam].append(husb)

                    elif key == "WIFE":
                        # We have a husband
                        for wife in FL[fam][key]:
                            famlist[fam].append(wife)



    except:
        logging.warning("[api/getTreeInformation][parents][warning] No Recorded Child -> Family Connection")
    return famlist

