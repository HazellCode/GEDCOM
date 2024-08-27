# 
# Author: Archie
# Date: 19/06/2022
# File Name: Tools
# Description: where they are actually run from
#
# Imports
from Tools.colour import colour

def APIDFromSOURList(SOURLIST):
    # We need to extract the keys from the dict
    keys = list(SOURLIST.keys())
    outlist = []
    for key in keys:
        outlist.append(SOURLIST[key].APID)
    if keys:
        return ", ".join(outlist)
    else:
        return colour.RED + "No APID found" + colour.END