# 
# Author: Archie
# Date: 22/06/2022
# File Name: getParentsFromFamily
# Description: look at the name plz thank ✨
#
# Imports
from Tools.colour import colour
def getParents(fam,FL,PL):
    i = 0
    outstr = ""
    if len(fam) <= 0:
        return colour.BOLD + colour.RED + "No Parents Found" + colour.END
    for f in fam:
        c = 0
        parentList = []
        if FL[f].HUSB:
            parentList.append(' '.join(PL[FL[f].HUSB].NAME.NAME_PERSONAL))
            c+=1
        if FL[f].WIFE:
            parentList.append(' '.join(PL[FL[f].WIFE].NAME.NAME_PERSONAL))
            c+=1
        if c > 1:
            outstr += "(" + colour.PURPLE + parentList[0] + colour.END + " and " + colour.PURPLE + parentList[1] + colour.END + ") - " + f
        else:
            outstr += "(" + colour.PURPLE + parentList[0] + colour.END + ") - " + f
        if len(fam) > 1 and (i+1)<len(fam):
            outstr += "\n                      "
        i += 1
    return outstr