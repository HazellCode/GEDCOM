# take in the id and personlist and return an array of objects
import logging

processedids = []
logging.basicConfig(level=logging.ERROR)
def getSiblingsOfIndividuals(indi,PL,FL):

    siblist = []

    if indi in processedids:
        return
    try:
        for fam in PL[indi]['FAMC']:
                # we now have the family where they are a child
                # if there are other children in this family get their objects and add them to the list
                # if there are no other children then just return a blank object as there are no siblings
                # this will repeat for every family this individual is a part of
            try:
                for chil in FL[fam]['CHIL']:

                    try:
                        logging.debug("[api/getTreeInformation][sibling][processing] CHIL - " + chil)

                        if chil != indi:
                                # i need to create a json object for the sibling so that js doesn't have a fucking fit
                                # could be a good idea to create an individial json template so that i dont waste storage space and then it will be ✨the most efficient✨
                                # you need to add parents to the sibling object as although they may not be directed related to the root they are still part of the tree.
                                # maybe implement a hiding feature to either minimise or straight ✨yeet✨ the non direct relations out of the tree

                                #### THIS LOOK AT THIS
                                # just add a sibling key to the makeSimpleTree generator and just recur over the
                                # sibling list instead of a parent list and it will generate the same attibutes for the siblings as it does paresnts and the first individual
                                ### PLEASE FOR THE LOVE OF GOD SEE THIS PLEASE MY FRIEND IN CHRIST
                            siblist.append(chil)
                            processedids.append(chil)
                            logging.debug("[api/getTreeInformation][sibling][success] - " + chil)


                    except Exception as e:
                        logging.error("[api/getTreeInformation][sibling][error] Sibling is referenced by does not exist - ID:  " + str(e))
            except Exception as e:
                logging.error("[api/getTreeInformation][sibling][error] No Children Found" + str(e))
                pass
                    # debug


        # ok so this isn't working, maybe append child to the parent object???
    except Exception as e:
        logging.error("[api/getTreeInformation][sibling][error] No Child -> Family Connection found " + str(e))
        pass
    return siblist



def getSiblingsOfIndividuals_rFam(indi,PL,FL):

    siblist = {}

    if indi in processedids:
        return
    if indi == "@I3023@":
        pass
    try:
        for fam in PL[indi]['FAMC']:
            siblist[fam] = []

            try:
                for chil in FL[fam]['CHIL']:

                    try:
                        logging.debug("[api/getTreeInformation][sibling][processing] CHIL - " + PL[chil]['id'])

                        if PL[chil]['id'] != indi:

                            siblist[fam].append(PL[chil]['id'])
                            processedids.append(PL[chil]['id'])
                            logging.debug("[sibling][success] - " + PL[chil]['id'])


                    except Exception as e:
                        logging.error("[api/getTreeInformation][sibling][error] Sibling is referenced by does not exist - ID:  " + str(e))
            except Exception as e:
                logging.error("[api/getTreeInformation][sibling][error] Family is referenced but doesn't exist.")
                return {}

                    # debug
    except Exception as e:
        logging.error("[api/getTreeInformation][sibling][error] Family doesn't exist")
        return {}


    # ok so this isn't working, maybe append child to the parent object???
    return siblist
