# 
# Author: Archie
# Date: 29/07/2022
# File Name: parserV2
# Description: 
#

# Imports
import operator
from functools import reduce


# This version will convert the file directly into JSON

def Parse(file):


    fL = file.splitlines()
    output = {}
    c = 0
    plist = []
    iobj = ""
    IC = 0
    importance_modifier = 0
    print(c)
    set = True
    append = False

    for L in fL:

        if c == 22947:
            pass
        L = L.strip()
        # Need to take the first letter of each line and use that to work out the importance of the line

        try:

            importance = int(L[0])
            IC = extendList(plist, importance, IC)
            if int(importance) == 0:
                IC = 0
                importance_modifier = 0
                plist = []
                try:
                    mcommand = L.split(" ")[2]
                    msub = L.split(" ")[1]
                except Exception as err:
                    # This means that this line only has two objects
                    mcommand = L.split(" ")[1]
                if mcommand == "HEAD":
                    output[mcommand] = {}
                    plist.insert(importance, "HEAD")
                else:
                    value = L.split(" ")[1]
                    if mcommand == "INDI":
                        if not 'People' in output:
                            output['People'] = {}
                        # This is creating a new person object in JSON
                        output['People'][value] = {}
                        output['People'][value]['id'] = value
                        plist.insert(importance, 'People')
                        plist.insert(importance + 1, value)
                        importance_modifier = 1
                        extendList(plist, importance, IC)
                    elif mcommand == "SUBM":
                        if not 'Submitters' in output:
                            output['Submitters'] = {}
                        output['Submitters'][value] = {}
                        plist.insert(importance, 'Submitters')
                        plist.insert(importance + 1, value)

                        importance_modifier = 1
                        extendList(plist, importance, IC)
                    elif mcommand == "FAM":
                        if not 'Family' in output:
                            output['Family'] = {}
                        # This is creating a new person object in JSON
                        output['Family'][value] = {}
                        plist.insert(importance, 'Family')
                        plist.insert(importance + 1, value)
                        importance_modifier = 1
                        extendList(plist, importance, IC)
                    elif mcommand == "OBJE":
                        if not 'Objects' in output:
                            output['Objects'] = {}
                        # This is creating a new person object in JSON
                        output['Objects'][value] = {}
                        plist.insert(importance, 'Objects')
                        plist.insert(importance + 1, value)
                        importance_modifier = 1
                        extendList(plist, importance, IC)
                    elif mcommand == "_PLAC" or msub == "_PLAC":
                        if not '_PLAC' in output:
                            output['_PLAC'] = {}
                        if msub == "_PLAC":
                            value = L.split(" ")[2]
                        # This is creating a new person object in JSON
                        output['_PLAC'][value] = {}
                        plist.insert(importance, '_PLAC')
                        plist.insert(importance + 1, value)
                        importance_modifier = 1
                        extendList(plist, importance, IC)
                    elif mcommand == "SOUR":
                        if not 'Sources' in output:
                            output['Sources'] = {}
                        # This is creating a new person object in JSON
                        output['Sources'][value] = {}
                        plist.insert(importance, 'Sources')
                        plist.insert(importance + 1, value)
                        importance_modifier = 1
                        extendList(plist, importance, IC)
                    elif mcommand == "REPO":
                        if not 'Repos' in output:
                            output['Repos'] = {}
                        # This is creating a new person object in JSON
                        output['Repos'][value] = {}
                        plist.insert(importance, 'Repos')
                        plist.insert(importance + 1, value)
                        importance_modifier = 1
                        extendList(plist, importance, IC)
                    else:
                        if not mcommand in output:
                            output[mcommand] = {}
                        plist.insert(importance, mcommand)



            elif int(importance) > 0:
                importance += importance_modifier
                extendList(plist, importance, IC)
                try:
                    command = L.split(" ")[1]

                    plist[importance] = command
                    plist = plist[:importance + 1]
                    IC = importance
                    ln = L.split(" ")
                    if len(ln) > 2:
                        value = ln[2:]
                        # We need to check that the attribute we are trying to write to is actually a dictionary

                        # Here we can have validation logic before the file is written to the json
                        if command == "CONT" or command == "CONC":
                            # We need to check that the note object is a list and not a dictionary
                            # This happens when NOTE is passed by the gedcom file but not given any arguments thus creating an object

                            if not isinstance(reduce(operator.getitem, plist[:-2], output)[plist[-2]], dict):
                                set = False
                            plist = plist[:importance]
                            IC -= 1
                        elif command == "CHIL":
                            try:
                                if reduce(operator.getitem, plist[:-1], output)[plist[-1]]:
                                    value = value[0]
                                    append = True
                                    set = False
                            except:
                                pass
                        elif command == "HUSB":
                            try:
                                if reduce(operator.getitem, plist[:-1], output)[plist[-1]]:
                                    pass
                            except:
                                output['Family'][plist[1]]['HUSB'] = []
                            append = True
                            set = False
                            value = {str(ln[2]): "F"}
                        elif command == "WIFE":
                            try:
                                if reduce(operator.getitem, plist[:-1], output)[plist[-1]]:
                                    pass
                            except:
                                output['Family'][plist[1]]['WIFE'] = []
                            append = True
                            set = False
                            value = {str(ln[2]): "M"}




                        else:
                            if not isinstance(reduce(operator.getitem, plist[:-2], output)[plist[-2]], dict):
                                # We need to make a copy of the data in the object
                                convertEntryToDictEntry(plist, output)

                            # Extra commands


                        if set:
                            reduce(operator.getitem, plist[:-1], output)[plist[-1]] = value
                        elif append:
                            reduce(operator.getitem, plist[:-1], output)[plist[-1]].append(value)
                        else:
                            reduce(operator.getitem, plist[:-1], output)[plist[-1]] += value
                        set = True
                        append = False
                    else:
                        value = None
                        if plist[-1] == "SURN":
                            reduce(operator.getitem, plist[:-1], output)[plist[-1]] = []
                        else:
                            reduce(operator.getitem, plist[:-1], output)[plist[-1]] = {}
                        # Here we have a command where only two objects where defined so we need to make a list to store potential child objectst
                        # We can clean this up later but that is a job for later

                        # We can also check for objects here

                        pass
                except Exception as err:
                    print("Line: " + str(c + 1))
                    print(err)

                    # plist[importance] = command

            # We now want to take the lines and append them to a JSON object


        except Exception as err:
            print("Line:" + str(L))
            print(err)
        # We then need to get the command
        c += 1

    return output


def extendList(list, importance, IC):
    if importance > IC:
        IC = importance
        list.append("")
    return IC


def convertEntryToDictEntry(plist, output):
    temp = reduce(operator.getitem, plist[:-2], output)[plist[-2]]
    reduce(operator.getitem, plist[:-2], output)[plist[-2]] = {}
    reduce(operator.getitem, plist[:-1], output)[plist[-2]] = temp


def convertEntryToListEntry(plist, output):
    temp = reduce(operator.getitem, plist[:-1], output)[plist[-1]]
    reduce(operator.getitem, plist[:-1], output)[plist[-1]] = []
    reduce(operator.getitem, plist[:-1], output)[plist[-1]] = temp
