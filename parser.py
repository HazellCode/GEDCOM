from Individual.Individual import Individual
from Family.FAM_RECORD import FAM



# We need to open the GEDCOM file or text file and process it
# 0 means the start of a new object



def parseFamilyTree(file):
    # Initalise the storage arrays
    PersonList = {}
    FamilyList = {}
    MetaData = {}
    # Open the file for the parser to read
    f = open(file,"r")
    fL = f.readlines()


    currentPerson = None
    currentFamily = None
    currentHead = None
    currentSubmitter = None
    levelParent = {1: ["",False,None],2: ["",""]}
    i = 0
    MetaData['Submitter'] = {}
    for L in fL:



        # We have the line now we need to read it and figure out what it wants
        # We first need to check what the first character of the line is
        if i == 14:
            pass
        if L == "\n":
            continue
        L = L.encode('ascii', 'ignore').decode('utf-8')
        L = L.split(" ")
        # we need to check if the first start contains /ufeff and strip it
        if L[0] == '0' and len(L) == 2:
            if L[1] == "HEAD\n":

                currentHead = True
        elif L[0] == '0':
            currentPerson = None
            currentHead = None
            currentFamily = None
            currentSubmitter = None
            # Reinitialise the source list
            levelParent[2] = ("", "")
            # We have a new record that we need to process
            # As it is a new record it will have three parts with the last being the type of record we are about to process
            if L[1] == "TRLR\n":
                continue
            elif L[2] == "INDI\n":
                # We are about to get an INDIvidual record to process
                PersonList[L[1]] = Individual(L[1])
                currentPerson = PersonList[L[1]]

            elif L[2] == "FAM\n":
                # We have a family record we need to process
                FamilyList[L[1]] = FAM(L[1])
                currentFamily = FamilyList[L[1]]

            elif L[2] == "OBJE\n":
                currentFamily = None
                currentPerson = None
            elif L[2] == "SUBM\n":
                currentSubmitter = str(L[1])

                MetaData['Submitter'][currentSubmitter] = {}
                levelParent[1][0] = ["SUBM"]


        if L[0] == '1' and currentHead:
            if L[1] == "GEDC\n":
                MetaData['GEDC'] = {}
                levelParent[1] = ["GEDC", False, False]
            elif L[1] == "CHAR":
                MetaData['CHAR'] = L[2]
                levelParent[1][0] = "CHAR"
            elif L[1] == "SOUR":
                MetaData['SOUR'] = {}
                levelParent[1][0] = "SOUR"
            elif L[1] == "LANG":
                MetaData['LANG'] = L[2]
                levelParent[1][0] = "LANG"
            elif L[1] == "COPR":
                MetaData['COPR'] = " ".join(L[2:])
                levelParent[1][0] = "COPR"
            elif L[1] == "NOTE":
                MetaData['NOTE'] = " ".join(L[2:]).strip("\n")
                levelParent[1][0] = "NOTE"
        elif L[0] == '1' and currentPerson:
            # Reinitialise the source list
            levelParent[2] = ("", "")
            # We are adding attributes to an object
            if L[1] == "RIN":
                currentPerson.RIN = L[2].strip()
            if L[1] == "_UID":
                currentPerson.UID = L[2].strip()
            if L[1] == "_UPD":
                currentPerson.UPD = " ".join(L[2:])
            if L[1] == "NOTE":
                currentPerson.NOTE = " ".join(L[2:])
                levelParent[1] = ["NOTE", False, None]

            if L[1] == 'NAME':
                currentPerson.NAME.NAME_PERSONAL.append(" ".join([i.strip('""').strip("//").strip("\n") for i in L[2:]]))
                levelParent[1] = ["NAME",False,None]

            elif L[1] == 'SEX':
                currentPerson.SEX.SEX = L[2].strip()
                levelParent[1] = ["SEX",False,None]

            elif L[1] == "FAMC":
                getattr(currentPerson, "FAMC")[L[2].strip()]
                levelParent[1] = ["FAMC", False, None]
                levelParent[2] = ("FAMC", L[2].strip())

            elif L[1] == "FAMS":
                getattr(currentPerson, "FAMS")[L[2].strip()]
                getattr(currentPerson, "FAMS")[L[2].strip()].FAMSID=[L[2].strip()]
                levelParent[1] = ["FAMS", False, None]
                levelParent[2] = ("FAMS", L[2].strip())

            elif L[1] == "SOUR":
                currentPerson.SOUR[L[2].strip()]
                levelParent[2] = ("SOUR," + L[2].strip()).split(",")

            elif L[1].strip() == "BIRT":
                levelParent[1] = ["BIRT",True,"EventDetail"]

            elif L[1].strip() == "DEAT":
                levelParent[1] = ["DEAT",True,"EventDetail"]

            elif L[1].strip() == "PROB":
                levelParent[1] = ["PROB",True,"EventDetail"]

            elif L[1].strip() == "BAPM":
                levelParent[1] = ["BAPM",True,"EventDetail"]

            elif L[1].strip() == "RESI":
                levelParent[1] = ["RESI", True, "EventDetail"]

            elif L[1].strip() == "BURI":
                levelParent[1] = ["BURI", True, "EventDetail"]

            elif L[1].strip() == "ADOP":
                levelParent[1] = ["ADOP", True, "EventDetail"]

            elif L[1].strip() == "OCCU":
                currentPerson.OCCU.JobDesc = ' '.join(L[2:]).strip()
                levelParent[1] = ["OCCU", True, "EventDetail"]


            # Processing Family Record Information at Level 1
        elif L[0] == '1' and currentSubmitter:
            if L[1] == "NAME":
                MetaData['Submitter'][currentSubmitter]['NAME'] = " ".join(L[2])
        if L[0] == '1' and currentFamily:
            if L[1].strip() == "HUSB":
                currentFamily.HUSB = L[2].strip()

            elif L[1].strip() == "WIFE":
                currentFamily.WIFE = L[2].strip()

            elif L[1].strip() == "CHIL":
                currentFamily.CHIL.append(L[2].strip())

            elif L[1].strip() == "MARR":
                currentFamily.MARR.MARR = True
                levelParent[1] = ["MARR", True, "FAMEventDetail"]
        elif L[0] == '2' and levelParent[2][0] == "SOUR":

            # Just source things

            if levelParent[2][0] == "SOUR":
                # This is a child of the SOUR_Link
                if L[1] == "PAGE":
                    currentPerson.SOUR[levelParent[2][1]].PAGE = L[2:]
                elif L[1] == "_APID":
                    currentPerson.SOUR[levelParent[2][1]].APID = L[2].strip()

        elif L[0] == '2':
            if currentPerson:
                if L[1] == "SOUR" and levelParent[1][1]:
                    # We create a new Source_Link record in
                    getattr(getattr(currentPerson, levelParent[1][0]).i_event_detail.event_detail, L[1])[L[2].strip()]
                    levelParent[2] = ("SOUR," + L[2].strip()).split(",")

                elif L[1] == "SOUR":
                    getattr(getattr(currentPerson, levelParent[1][0]), L[1])[L[2].strip()]
                    levelParent[2] = ("SOUR," + L[2].strip()).split(",")

                elif levelParent[1][0] == "FAMC":
                    if L[1] == "PEDI":
                        currentPerson.FAMC[levelParent[2][1].strip()].PEDI = L[2].strip()

                elif levelParent[1][0] == "NAME":
                    if L[1] == "SURN":
                        currentPerson.NAME.PERSONAL_NAME_PIECES.SURNAME = L[2].strip().strip("//")
                    elif L[1] == "GIVN":
                        currentPerson.NAME.PERSONAL_NAME_PIECES.GIVEN = [i.strip('""') for i in L[2:]]

                elif levelParent[1][0] == "NOTE":
                    if L[1] == "CONT":
                        currentPerson.NOTE += " ".join(L[2:])

                elif levelParent[1][2] == "EventDetail":
                    if L[1] == "DATE":
                        getattr(currentPerson, levelParent[1][0]).i_event_detail.event_detail.DATE = '/'.join(L[2:]).strip()
                    elif L[1] == "PLAC":
                        getattr(currentPerson, levelParent[1][0]).i_event_detail.event_detail.PLACE.PLAC.PLAC = ' '.join(L[2:]).strip()
                    elif L[1] == "RIN":
                        getattr(currentPerson, levelParent[1][0]).i_event_detail.RIN = ' '.join(L[2:]).strip()
            elif currentFamily:
                if levelParent[1][2] == "FAMEventDetail":
                    if L[1] == "DATE":
                        getattr(currentFamily, levelParent[1][0]).f_event_detail.event_detail.DATE = '/'.join(L[2:]).strip()
                    elif L[1] == "PLAC":
                        getattr(currentFamily, levelParent[1][0]).f_event_detail.event_detail.PLACE.PLAC.PLAC = ' '.join(L[2:]).strip()
            elif levelParent[1][0] == "GEDC" and currentHead:
                if L[1] == "VERS":
                    ver = L[2].split(".")
                    try:
                        if int(ver[0]) > 5:
                            raise ValueError('GEDCOM ' + str(int(ver[0])) + ".x.x is not supported")
                        elif int(ver[1]) > 5:
                            raise ValueError('GEDCOM ' + str(int(ver[0])) + "." + str(int(ver[1])) + ".x is not supported")
                        elif int(ver[2]) > 2:
                            raise ValueError('GEDCOM ' + str(int(ver[0])) + "." +  str(int(ver[1])) + "." +  str(int(ver[2])) + " is not supported")
                        MetaData['GEDC']['VERS'] = {}
                        MetaData['GEDC']['VERS'] = L[2]
                    except Exception as err:
                        print('Error: ' + repr(err))
                        break
                if L[1] == "FORM":
                    MetaData['GEDC']['FORM'] = {}
                    MetaData['GEDC']['FORM'] = L[2]
            elif levelParent[1][0] == "SOUR" and currentHead:
                if L[1] == "VERS":
                    MetaData['SOUR']['VERS'] = {}
                    MetaData['SOUR']['VERS'] = L[2]
            elif levelParent[1][0] == "NOTE" and currentHead:
                if L[1] == "CONT":
                    MetaData['NOTE'] = MetaData['NOTE'] + " " +  " ".join(L[2:]).strip("\n")
        elif L[0] == '3':
            if currentPerson:
                if levelParent[2][0] == "SOUR" and levelParent[1][1]:
                    # This is a child of the SOUR_Link
                    if L[1] == "PAGE":
                        getattr(currentPerson, levelParent[1][0]).i_event_detail.event_detail.SOUR[levelParent[2][1]].PAGE = L[2:]
                    elif L[1] == "_APID":
                        getattr(currentPerson, levelParent[1][0]).i_event_detail.event_detail.SOUR[levelParent[2][1]].APID = L[2].strip()
                elif levelParent[2][0] == "SOUR":
                    # This is a child of the SOUR_Link
                    if L[1] == "PAGE":
                        getattr(currentPerson, levelParent[1][0]).SOUR[levelParent[2][1]].PAGE = L[2:]
                    elif L[1] == "_APID":
                        getattr(currentPerson, levelParent[1][0]).SOUR[levelParent[2][1]].APID = L[2].strip()
            elif currentFamily:
                if levelParent[2][0] == "SOUR" and levelParent[1][1]:
                    # This is a child of the SOUR_Link
                    if L[1] == "PAGE":
                        getattr(currentFamily, levelParent[1][0]).f_event_detail.event_detail.SOUR[levelParent[2][1]].PAGE = L[
                                                                                                                             2:]
                    elif L[1] == "_APID":
                        getattr(currentFamily, levelParent[1][0]).f_event_detail.event_detail.SOUR[levelParent[2][1]].APID = L[
                            2].strip()
                elif levelParent[2][0] == "SOUR":
                    # This is a child of the SOUR_Link
                    if L[1] == "PAGE":
                        getattr(currentFamily, levelParent[1][0]).SOUR[levelParent[2][1]].PAGE = L[2:]
                    elif L[1] == "_APID":
                        getattr(currentFamily, levelParent[1][0]).SOUR[levelParent[2][1]].APID = L[2].strip()
        i += 1


    return PersonList, FamilyList







