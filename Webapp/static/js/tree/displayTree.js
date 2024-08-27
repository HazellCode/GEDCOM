
if (!window.localStorage['tree_uuid']){
    window.localStorage['tree_uuid'] = null
}
// Aight we know need some fetch shit
        window.addEventListener('load',function (){


            // We need to get the rootindi from local storage then make an ajax request to flask to get the data
            fetch("/api/getTreeInformation",{
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({"id": window.localStorage['rootindi'],"uuid": window.localStorage['tree_uuid']})

            })
                .then(res => res.json())
                .then(data => {

                    if (data.data !== "_304"){
                        window.localStorage['tree_uuid'] = data.uuid
                        storeIndi(dbprom,data.data).then(initalisetree(data.ctime))
                    } else {
                        initalisetree()
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

function initalisetree(ctime){

            let rootindi = window.localStorage['rootindi']

            const treediv = document.querySelector('#family_tree')
            const queryString = window.location.search;
            const urlParam = new URLSearchParams(queryString)
            console.log(ctime)
            const ctimeobj = document.getElementById("completed-time")
            if (ctime !== undefined){

                ctimeobj.textContent = "Generated in " + ctime + "s"
            } else {
                ctimeobj.textContent = "Using local data"
            }



            dbprom.then(async function(db){
                let res = {}
                let cur = await db.transaction('individuals').store.openCursor();
                while (cur) {
                    res[cur.key] = cur.value
                    cur = await cur.continue();
                }
                return res
            }).then(function(val) {
                treejson1 = val









                genlock = 0;
                maxgeneration = 0;

                // if (treejson1.hasOwnProperty('error')){
                //     // We wanna print some html to display the error to the user
                //     // For now ima just print it to the console
                //     console.log("Error: " + treejson1.error)
                //     console.log("Reason: " + treejson1.reason)
                //     const errorcontainer = treediv.appendChild(document.createElement("div"))
                //     const errorcontainerchil = errorcontainer.appendChild(document.createElement("div"))
                //     const errordisplay = errorcontainerchil.appendChild(document.createElement("h1"))
                //     const errorcode = errorcontainerchil.appendChild(document.createElement("h2"))
                //     const errorreason = errorcontainerchil.appendChild(document.createElement("h5"))
                //
                //     errorcontainer.classList.add("container","mt-3")
                //     errorcontainerchil.classList.add("mt-4","p-5", "text-white", "rounded", "divbg")
                //     errorreason.classList.add("mt-2")
                //     errordisplay.classList.add("mb-5")
                //     errordisplay.textContent = "ERROR"
                //     errorcode.textContent = treejson1.error
                //     errorreason.textContent = treejson1.reason



                    dbprom.then(async function(db){
                        let res = {}
                        let cur = await db.transaction('individuals').store.index("generation").openCursor(null,"prev");

                        return cur.value.generation
                    }).then(function(val) {
                        if (val){

                            maxgeneration = val;
                        }


                        genlock = 4
                        let genselect = document.querySelector("#genselectplaceholder").appendChild(document.createElement('select'))

                        if (urlParam.get('generation')) {
                            let edited = 0
                            if (urlParam.get('generation') > maxgeneration) {
                                genlock = maxgeneration
                                console.log("Please enter a generation between 0 and " + maxgeneration + " inclusive")
                                edited = 1
                            }

                            if (urlParam.get('generation') < 0 ) {
                                console.log(urlParam.get('generation'))
                                genlock = 0
                                edited = 1
                            }
                            if (edited === 0){
                                genlock = urlParam.get('generation')
                            }
                        } else {

                            genlock = maxgeneration;
}



                        genselect.className = "form-select form-select-sm nav-link w-auto"
                        genselect.style = "width:100%; "
                        genselect.id = "generationSelector"
                        genselect.name = "generationSelector"


                        for (let i = 0; i <= maxgeneration; i++) {
                            let option = genselect.appendChild(document.createElement("option"))
                            option.id = "gens-" + i;
                            option.className = "inline";
                            option.textContent = "Generation " + i;
                        }
                        genselect.onchange = function (event) {
                            return reloadpagewithgeneration(event.target)
                        };

                        genselect.selectedIndex = genlock

                        //We need to read the url parameters to get the generation lock, if there are no parameters then we will use no lock



                        let UL = treediv.appendChild(document.createElement('ul'))
                        processedids = []
                        buildtree(treejson1, treediv, UL,rootindi)

                        // We finnally need to scroll the user to the very middle of the webpage

                        midpoint = document.getElementById("div"+rootindi);
                        midpoint.scrollIntoView({
                            behavior: "auto",
                            block: "center",
                            inline: "center"
                        });
                        $(function () {
                        const popoverTriggerList = document.querySelectorAll('[data-toggle="popover"]')
                        const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))

                    })




                    })






            })
}

function buildtree(localtree, treediv, mUL,rootindi) {

                            currentobj = localtree[rootindi]
                            if (processedids.includes(currentobj.id)){

                            } else {



                                processedids.push(currentobj.id)

                                if (currentobj.generation > genlock) {
                                    return
                                }


                                let LI = mUL.appendChild(document.createElement('li'))
                                LI.id = currentobj.id
                                let hovermenu = LI.appendChild(document.createElement('div'))
                                let indidiv = LI.appendChild(document.createElement('div'))
                                indidiv.id = "div" + currentobj.id
                                let a = indidiv.appendChild(document.createElement('a'))
                                let born = indidiv.appendChild(document.createElement("p"))

                                // we need to give the indi div a class so that it can be styled
                                indidiv.className = 'treeIndiBG'
                                try {
                                    a.innerHTML = currentobj.data.NAME.GIVN.join(" ")
                                } catch {
                                    console.log(currentobj)
                                    a.innerHTML = currentobj.data.NAME.NAME
                                }

                                a.innerHTML += `<b> ${currentobj.data.NAME.SURN}</b>`

                                // This is to make the popover work
                                // We need to add an event listener that we can address in base


                                a.setAttribute("role", "button")

                                a.setAttribute("tabindex", "0")
                                a.setAttribute("data-toggle", "popover")
                                a.setAttribute("data-bs-custom-class", "custom-popover")
                                a.setAttribute("data-bs-trigger", "focus")
                                a.setAttribute("data-bs-placement", "bottom")
                                a.setAttribute("title", "Information")
                                a.setAttribute("data-bs-html", "true")

                                // before we add content to the popover we need to get the parents for the individual and then turn it into html
                                // potentially have them as <a> so that they can be clicked on and take you to the big info page


                                // Get data to be shown in popover


                                let html = `<div class="popovercard" id="popover+${currentobj.id}">
                                    <a  id="pl${currentobj.id}"class="popovertext popover-text-title">${getDataFromJSON(currentobj.data,['NAME','GIVN']).join(" ")}</a>
                                    <h6 class="popovertext popover-text-lower"><span class="popover-text-bold">Born: ${getDataFromJSON(currentobj.data,['BIRT','DATE'])}</span></h6>
                                    <h6 class="popovertext popover-text-lower"><span class="popover-text-bold">Sex:</span> ${getDataFromJSON(currentobj.data,['SEX'])}</h6>
                                    <h6 class="popovertext popover-text-lower"><span class="popover-text-bold">Parents:</span></h6>
                                    <ul>`


                                parents = currentobj.parents;


                                if (parents.length > 0) {
                                    let parname

                                    for (par in parents) {
                                        console.log(par)
                                        console.log(parents)
                                        console.log(parents[par])
                                        if (typeof(parents[par]) === 'object'){
                                            console.log(parents[par])
                                            par = localtree[Object.keys(parents[par])[0]]
                                        } else {
                                            par = localtree[parents[par]]
                                        }


                                        console.log(par)

                                        try {

                                            parname = par.data.NAME.GIVN.join(" ")

                                        } catch {

                                            parname = localtree[par].data.NAME.NAME
                                        }


                                        html += `<li class="popoverparent"><a href="#" id="pl${par.id}" class="popoverlink">${parname} >></a></li>`


                                    }
                                    html += `</ul>`
                                } else {
                                    html += `<li class="popoverparent">No Parents Found</li></ul>`
                                }
                                html += `<h6 class="popovertext popover-text-lower"><span class="popover-text-bold">Siblings:</span></h6><ul>`
                                siblings = currentobj.ochil;
                                if (siblings.length > 0) {
                                    let sibname

                                    for (sib in siblings) {
                                        try {
                                            sibname = localtree[siblings[sib]].data.NAME.GIVN.join(" ")
                                        } catch {
                                            sibname = localtree[siblings[sib]].data.NAME.NAME
                                        }
                                        html += `<li class="popoverparent"><a href="#" id="pl${localtree[siblings[sib]].id}" class="popoverlink">${sibname} >></a></li>`


                                    }
                                    html += `</ul>`
                                } else {
                                    html += `<li class="popoverparent">No Siblings Found</li>`
                                }

                                html = html + `</div>`
                                a.setAttribute("data-bs-content",
                                    html)
                                born.textContent = getDataFromJSON(currentobj.data,['BIRT','DATE'])
                                born.className = "born"

                                // Hover menu


                                //console.log("Name: ", localtree.name," Number of Parents: " + localtree.parents)

                                if (currentobj.parents.length > 0) {

                                    let UL = LI.appendChild(document.createElement('ul'))
                                    let newtree = LI
                                    for (par of currentobj.parents) {
                                        console.log(par)

                                        if (typeof(par) === 'object'){

                                            par = Object.keys(par)[0]
                                        }
                                        console.log(par)
                                        buildtree(localtree, newtree, UL, par)
                                    }


                                } else {
                                    <!--treediv.appendChild(document.createElement('ul'))-->
                                    return
                                }


                                // Add an event listener to the popover buttons

                            }
                        }



