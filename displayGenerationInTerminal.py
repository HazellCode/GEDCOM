# 
# Author: Archie
# Date: 22/06/2022
# File Name: displayGenerationInTerminal.py
# Description: 
#
# Imports
from Family.showFamily import showFamily
from Family.getChildrenOfIndividual import getChildrenOfIndividual
from Family.makeFamilyTree import makeFamilyTree
from parser import parseFamilyTree
from Tools.Tools import APIDFromSOURList
from Tools.colour import colour
from Tools.getParentsFromFamily import getParents
from Tools.getChildrenFromFamily import getChildren



#getChildrenOfIndividual("@I262196771608@", PersonList, FamilyList,0)

PersonList, FamilyList = parseFamilyTree("Family Tree-no header.ged")
genlist = makeFamilyTree("@I262196792752@", PersonList, FamilyList,0)

for gen in reversed(genlist):
    print(colour.BOLD + colour.CYAN + "Generation: " + str(gen) + "\n" + colour.END)
    for indi in genlist[gen]:
        print(colour.BOLD + colour.GREEN + ' '.join(PersonList[indi].NAME.NAME_PERSONAL) + "\n" + colour.END)
        print(colour.BOLD + "     - Child  of    - " + colour.END +
                  getParents(list(PersonList[indi].FAMC.keys()),FamilyList,PersonList)
              )
        print(colour.BOLD + "     - Parent of    - " + colour.END +
                  getChildren(list(PersonList[indi].FAMS.keys()),FamilyList,PersonList)
              )
        print(colour.BOLD + "     - Sex          - " + colour.END + str(PersonList[indi].SEX.SEX))
        print(colour.BOLD + "     - Born         - " + colour.END + str(PersonList[indi].BIRT.i_event_detail.event_detail.DATE))
        print(colour.BOLD + "         - Place      - " + colour.END + str(PersonList[indi].BIRT.i_event_detail.event_detail.PLACE.PLAC.PLAC))
        print(colour.BOLD + "     - Died         - " + colour.END + str(PersonList[indi].DEAT.i_event_detail.event_detail.DATE))
        print(colour.BOLD + "         - Place      - " + colour.END + str(PersonList[indi].DEAT.i_event_detail.event_detail.PLACE.PLAC.PLAC))
        print(colour.BOLD + "     - Residence    - " + colour.END + str(PersonList[indi].RESI.i_event_detail.event_detail.PLACE.PLAC.PLAC))
        print(colour.BOLD + "         - Date       - " + colour.END + str(PersonList[indi].RESI.i_event_detail.event_detail.DATE))
        print(colour.BOLD + "             - APID    - " + colour.END +  str(APIDFromSOURList(PersonList[indi].RESI.i_event_detail.event_detail.SOUR)))


        print("\n")

    print("\n")
