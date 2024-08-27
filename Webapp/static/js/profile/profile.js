//
// Author: Archie
// Date: 30/06/2022
// File Name: profile.js
// Description:
//
// Imports



window.addEventListener('load',getIndividualData())
let GEDLIST = ["BIRT", "RESI", "SEX"] // GEDCOM Fact Descriptor List
function getIndividualData(){
    individuals = []
    individuals.push(window.localStorage['sel_id'])
    fetch("/api/getAllDataIndividual",{
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({"id":individuals})

            })
                .then(res => res.json())
                .then(data => {

                    if (data.data !== "_304") {


                        //This isn't working
                        storeDetail(dbprom,data.data).then(function(){
                            buildProfile(data.data)
                        })

                    }
                    // else {
                    // There has been no change to the data and we can use whatever we already have
                    // bear in mined this doesn't account for if the cache has been cleared since last reload so we need to try and send a guid to flask to check if they are the same
                    // idk it could even be quicker to do a hash but that probably wont work as well as a guid get and post.
                    // {

                })
                .catch((err) => {
                    console.log(err)
                })
}


function buildProfile(data) {
    focused_Indi = data[window.localStorage['sel_id']]
    // We need to display the data returned from the fetch to the db.
    let intarname = document.getElementById("indi-target-name")
    let intarborn = document.getElementById("indi-target-born")
    let intardeath = document.getElementById("indi-target-death")

    intarname = intarname.appendChild(document.createElement("span"))
    intarname.textContent = focused_Indi.NAME.NAME.join(" ")

    intarborn = intarborn.appendChild(document.createElement("span"))
    intarborn.innerHTML = "BORN in " + `<span class='indi-target-born-place'> ${getDataFromJSON(focused_Indi,['BIRT','PLAC'])} </span>`+ " on the " + `<span class='indi-target-born-date'>${getDataFromJSON(focused_Indi,['BIRT','DATE'])}</span>`

    intardeath = intardeath.appendChild(document.createElement("span"))
    console.log(getDataFromJSON(focused_Indi,['DEAT','DATE']))
    if (getDataFromJSON(focused_Indi,['DEAT','DATE']) !== "Present"){
        intardeath.innerHTML = "DIED in " + `<span class='indi-target-died-place'> ${getDataFromJSON(focused_Indi,['DEAT','PLAC'])} </span>` + " on the " + `<span class='indi-target-died-date'>${getDataFromJSON(focused_Indi,['DEAT','DATE'])}</span>`
    } else {
        intardeath.innerHTML = "Individual Has Not Died Yet"

    }
    displayParents(focused_Indi.PARENTS).then(function(res){
        displaySiblings(focused_Indi.SIBLINGS)
    })

    displayFacts(focused_Indi)

    displaySpouce(focused_Indi.FAMS).then(function(res){

    })



    // We are now going to display the when this record was last updated at the bottom of the profile block
    let pfb = document.getElementById("profile-block-footer")
    let pfb_upd = pfb.appendChild(document.createElement("span"))
    pfb_upd.className = "pfb_upd"
    pfb_upd.textContent = "Last Updated: " + focused_Indi.UPD



}

// These functions build the first and third columns of the profile page
function displayParents(parentList){
    return new Promise( function(resolve){

        fetch("/api/getAllDataIndividual",{
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({"id":parentList,"input_opt":"f"})

            })
                .then(res => res.json())
                .then(data => {

                    if (data.data !== "_304") {

                        // We will need to store these results at some point
                        parentContainer = document.getElementById("profile-content-parent-container")

                        for (fam in data.data){

                            familyContainer = parentContainer.appendChild(document.createElement("div"))
                            familyContainer.className = "profile-content-family-container"
                            familyContainer.id = "div-p-"+fam
                            familyDesignator = familyContainer.appendChild(document.createElement("div"))
                            familyDesignator.className = "profile-content-family-container-text"
                            familyDesignator.textContent = "Family ID: " + fam
                            for (p in data.data[fam]){

                                currentParent = data.data[fam][p]
                                let parentObj = familyContainer.appendChild(document.createElement("div"))
                                parentObj.className = 'profile-content-parent-obj'



                                let parentName = parentObj.appendChild(document.createElement("div"))
                                parentName.className = "profile-content-parent-obj-name"
                                parentName.textContent = getDataFromJSON(currentParent,['NAME','NAME']).join(" ")



                                 let parentRelation = parentObj.appendChild(document.createElement("div"))
                                parentRelation.className = "profile-content-parent-obj-relation"
                                parentRelation.textContent = getRelation(getDataFromJSON(currentParent,['relation']))


                                let parentTime = parentObj.appendChild(document.createElement("div"))
                                parentTime.className = "profile-content-parent-obj-time"
                                parentTime.textContent = getDataFromJSON(currentParent,['BIRT','DATE']) + " - " + getDataFromJSON(currentParent,['DEAT','DATE'])




                            }


                        }

                        resolve(true)





                    }
                    // else {
                    // There has been no change to the data and we can use whatever we already have
                    // bear in mined this doesn't account for if the cache has been cleared since last reload so we need to try and send a guid to flask to check if they are the same
                    // idk it could even be quicker to do a hash but that probably wont work as well as a guid get and post.
                    // {

                })
                .catch((err) => {
                    console.log(err)
                })


    })

}
function displaySiblings(siblist){

    fetch("/api/getAllDataIndividual",{
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({"id":siblist,"input_opt":"f"})

            })
                .then(res => res.json())
                .then(data => {

                    if (data.data !== "_304") {

                        // We will need to store these results at some point


                        for (fam in data.data){
                            parentContainer = document.getElementById("div-p-"+fam)
                            childContainer = parentContainer.appendChild(document.createElement("div"))
                            childContainer.className = "profile-content-child-container"


                            for (p in data.data[fam]){

                                currentParent = data.data[fam][p]
                                let parentObj = childContainer.appendChild(document.createElement("div"))
                                parentObj.className = 'profile-content-sibling-obj'

                                let siblingObj = parentObj.appendChild(document.createElement("div"))
                                siblingObj.className = 'profile-content-child-obj'



                                let parentName = siblingObj.appendChild(document.createElement("div"))
                                parentName.className = "profile-content-child-obj-name"
                                parentName.textContent = getDataFromJSON(currentParent,['NAME','NAME']).join(" ")






                                let parentTime = siblingObj.appendChild(document.createElement("div"))
                                parentTime.className = "profile-content-child-obj-time"
                                parentTime.textContent = getDataFromJSON(currentParent,['BIRT','DATE']) + " - " + getDataFromJSON(currentParent,['DEAT','DATE'])
                            }
                        }




                    }
                    // else {
                    // There has been no change to the data and we can use whatever we already have
                    // bear in mined this doesn't account for if the cache has been cleared since last reload so we need to try and send a guid to flask to check if they are the same
                    // idk it could even be quicker to do a hash but that probably wont work as well as a guid get and post.
                    // {

                })
                .catch((err) => {
                    console.log(err)
                })

}
function displaySpouce(fL){
    return new Promise( function(resolve){
        familyList = {}

        for (fam in fL){

            familyList[fL[fam]] = fL[fam]
        }


        fetch("/api/getFamilyData",{
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({"data":familyList,"input_opt":"s"})

            })
                .then(res => res.json())
                .then(data => {
                    if (data.error){

                        parentContainer = document.getElementById("profile-content-spouce-container")
                        errordiv = parentContainer.appendChild(document.createElement("div"))
                        errortitle = errordiv.appendChild(document.createElement("span"))
                        errortitle.textContent = data.error
                        errortitle.className = "profile-content-spouce-error-message"
                    } else {


                        if (data.data !== "_304") {

                            for (fam in data) {
                                parentContainer = document.getElementById("profile-content-spouce-container")
                                familyContainer = parentContainer.appendChild(document.createElement("div"))
                                familyContainer.className = "profile-content-family-container"
                                familyContainer.id = "div-c-s-" + fam
                                familyDesignator = familyContainer.appendChild(document.createElement("div"))
                                familyDesignator.className = "profile-content-family-container-text-right"
                                familyDesignator.textContent = "Family ID: " + fam
                                for (parent in data[fam]['parents']) {

                                    currentParent = data[fam]['parents'][parent]
                                    let parentObj = familyContainer.appendChild(document.createElement("div"))
                                    parentObj.className = 'profile-content-parent-obj'


                                    let parentName = parentObj.appendChild(document.createElement("div"))
                                    parentName.className = "profile-content-parent-obj-name"
                                    parentName.textContent = getDataFromJSON(currentParent,['NAME','NAME']).join(" ")


                                    let parentTime = parentObj.appendChild(document.createElement("div"))
                                    parentTime.className = "profile-content-parent-obj-time"
                                    parentTime.textContent = getDataFromJSON(currentParent,['BIRT','DATE']) + " - " + getDataFromJSON(currentParent,['DEAT','DATE'])

                                    if (currentParent.ID == localStorage['sel_id']) {
                                        parentObj.className = 'profile-content-parent-obj-focusedid'
                                        parentTime.className = "profile-content-parent-obj-time-focusedid"

                                    }
                                }
                            }
                            for (fam in data) {
                                parentContainer = document.getElementById("div-c-s-" + fam)
                                childContainer = parentContainer.appendChild(document.createElement("div"))
                                childContainer.className = "profile-content-child-container"
                                for (child in data[fam]['children']) {

                                    currentChild = data[fam]['children'][child]


                                    let parentObj = childContainer.appendChild(document.createElement("div"))
                                    parentObj.className = 'profile-content-sibling-obj-right'



                                    if (Object.keys(currentChild).length === 0){
                                        // The individual doesn't exsit but we still want to display it
                                        let siblingObj = parentObj.appendChild(document.createElement("div"))
                                        siblingObj.className = 'profile-content-child-obj-right'


                                        let parentName = siblingObj.appendChild(document.createElement("div"))
                                        parentName.className = "profile-content-child-obj-name"
                                        parentName.textContent = "Unknown Child"


                                        let parentTime = siblingObj.appendChild(document.createElement("div"))
                                        parentTime.className = "profile-content-child-obj-time"
                                        parentTime.textContent = "Unknown" + " - " + "Unknown"
                                    } else{
                                        let siblingObj = parentObj.appendChild(document.createElement("div"))
                                        siblingObj.className = 'profile-content-child-obj-right'


                                        let parentName = siblingObj.appendChild(document.createElement("div"))
                                        parentName.className = "profile-content-child-obj-name"
                                        parentName.textContent = getDataFromJSON(currentChild,['NAME','NAME']).join(" ")


                                        let parentTime = siblingObj.appendChild(document.createElement("div"))
                                        parentTime.className = "profile-content-child-obj-time"
                                        parentTime.textContent = getDataFromJSON(currentChild,['BIRT','DATE'])+ " - " + getDataFromJSON(currentChild,['DEAT','DATE'])
                                    }




                                }
                            }


                        }


                    }
                    resolve(true)






                    // else {
                    // There has been no change to the data and we can use whatever we already have
                    // bear in mined this doesn't account for if the cache has been cleared since last reload so we need to try and send a guid to flask to check if they are the same
                    // idk it could even be quicker to do a hash but that probably wont work as well as a guid get and post.
                    // {

                })
                .catch((err) => {
                    console.log(err)
                })


    })

}


function displayFacts(data){
    // Using a list of recognised GEDCOM objects we need to find them in the parsed data and display the facts to the user
    // There is probably an easier way to do this but idfk
    const fact_list = Object.keys(data).filter(e => GEDLIST.includes(e))
    parentContainer = document.getElementById("profile-content-facts-container")
    fact_list.forEach(function (fact,idx){
        containerDIV = parentContainer.appendChild(document.createElement("div"))
        containerDIV.id = "Facts-"+fact+"-container"
        containerDIV.className = "Facts-container"
        // Birth Fact

        if (fact === "BIRT"){
            // If we have a birth fact we want to display the place, date and if its there the reference or SOUR value
            // We need to create html objects for these elements in the middle column of the page
            // Date
            // Place
            let title = containerDIV.appendChild(document.createElement("div"))
                                title.id = "profile-content-facts-"+fact+"-title"
                                title.className = "profile-content-facts-title"
                                title.textContent = "Born"
            childDIV = containerDIV.appendChild(document.createElement("div"))
            childDIV.id = "Facts-"+fact+"-container-child"
            childDIV.className = "Facts-info-container"
            let place = childDIV.appendChild(document.createElement("div"))
                                place.id = "profile-content-facts-"+fact+"-place"
            place.innerHTML = "<span class='profile-content-facts-sub-title'>Place: </span>"+ getDataFromJSON(data,[fact,'PLAC'])
            let date = childDIV.appendChild(document.createElement("div"))
                                date.id = "profile-content-facts-"+fact+"-date"
                                date.innerHTML = "<span class='profile-content-facts-sub-title'>Date: </span>" + getDataFromJSON(data,[fact,'DATE'])




        }
        else if (fact === "RESI"){
            // If we have a birth fact we want to display the place, date and if its there the reference or SOUR value
            // We need to create html objects for these elements in the middle column of the page
            // Date
            // Place
            let title = containerDIV.appendChild(document.createElement("div"))
                                title.id = "profile-content-facts-"+fact+"-title"
                                title.className = "profile-content-facts-title"
                                title.textContent = "Address"
            childDIV = containerDIV.appendChild(document.createElement("div"))
            childDIV.id = "Facts-"+fact+"-container-child"
            childDIV.className = "Facts-info-container"
            let place = childDIV.appendChild(document.createElement("div"))
                                place.id = "profile-content-facts-"+fact+"-place"
            place.innerHTML = "<span class='profile-content-facts-sub-title'>Place: </span>"+ getDataFromJSON(data,[fact,'PLAC'])
            let date = childDIV.appendChild(document.createElement("div"))
                                date.id = "profile-content-facts-"+fact+"-date"
                                date.innerHTML = "<span class='profile-content-facts-sub-title'>Date: </span>" + getDataFromJSON(data,[fact,'DATE'])



        }
        else if (fact === "SEX"){
            // If we have a birth fact we want to display the place, date and if its there the reference or SOUR value
            // We need to create html objects for these elements in the middle column of the page
            // Date
            // Place
             let title = containerDIV.appendChild(document.createElement("div"))
                                title.id = "profile-content-facts-"+fact+"-title"
                                title.className = "profile-content-facts-title"
                                title.textContent = "Sex"
            childDIV = containerDIV.appendChild(document.createElement("div"))
            childDIV.id = "Facts-"+fact+"-container-child"
            childDIV.className = "Facts-info-container"
            let sex = childDIV.appendChild(document.createElement("div"))
                                sex.className = "profile-content-facts-"+fact+"-date"
                                sex.innerHTML = getDataFromJSON(data,[fact])




        }






    })

}








function getRelation(rel){
    if (rel === "F") {
        return "  - Father"
    } else if (rel === "M"){
        return "  - Mother"
    }

}







