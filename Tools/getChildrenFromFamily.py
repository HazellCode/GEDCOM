# 
# Author: Archie
# Date: 22/06/2022
# File Name: getChildrenFromFamily
# Description: yes were doing it againnnnn
#
# Imports
from Tools.colour import colour

def getChildren(fam,FL,PL):
    i = 0
    outstr = ""
    if len(fam) <= 0:
        return colour.BOLD + colour.RED + "No Children Found" + colour.END
    for f in fam:
        if f == "@F52@":
            pass
        childList = []
        for chil in FL[f].CHIL:
            childList.append(' '.join(PL[chil].NAME.NAME_PERSONAL))
        if len(childList) <= 0:
            return colour.BOLD + colour.RED + "No Children Found" + colour.END
        if len(childList) > 1:
            if len(childList) == 2:
                outstr += "(" + colour.GREEN + childList[0] + colour.END + " and " + colour.GREEN + childList[1] + colour.END+") - " + f
            else:
                outstr += "("
                for i in range(0, len(childList)-1):
                    outstr += colour.GREEN + childList[i] + colour.END
                    if i <= len(childList)-3:
                        outstr += ", "
                outstr += " and " + colour.GREEN + childList[len(childList)-1] + colour.END + ") - " + f
        else:
            outstr += "(" + colour.GREEN + childList[0] + colour.END + ") - " + f
        if len(fam) > 1 and (i+1)<len(fam):
            outstr += "\n                      "
        i += 1
    return outstr