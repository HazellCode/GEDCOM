function getDataFromJSON(json, key){

    try{
        completekey
    } catch {
        completekey = key
        flag = ""
         console.log(key)
        if (compareArray(key, ['SEX'])){
            flag = "s_"
        } else if (compareArray(key, ['DEAT',"DATE"])){
            flag = "date_"
        }
    }
    try{

    } catch{
        console.log("flag not defined yet")
    }



    while (key.length > 0) {
        try {

            return getDataFromJSON(json[key[0]],key.slice(1))
        } catch (err) {
            if (compareArray(completekey,['DEAT','DATE'])){
                return "Present"
            } else {
                return "Unknown"
            }

        }
    }

    if (flag === "s_"){
        if (compareArray(json,["M"])){
            json = ["Male"]
        } else if (compareArray(json,["F"])){
            json = ["Female"]

        } else if (compareArray(json,["O"]) || compareArray(json,["X"])  ){
            json = ["Other"]
        } else if (compareArray(json,["NB"])){
            json = ["Non-Binary"]
        } else if (compareArray(json,["TM"])){
            json = ["Trans-Man"]
        } else if (compareArray(json,["TW"])){
            json = ["Trans-Woman"]
        }
    }

    if (flag === "date_"){
        console.log("DATE FOUND")
        console.log(completekey)
        console.log(json)
        console.log(json)
        if (!!~json[0].includes("/")){
            json = json.join(("/"))
        } else {

        }
    }


    delete flag
    delete completekey
    return json
}

function compareArray(a,b){
    return Array.isArray(a) && Array.isArray(b) && a.every((val,index) => val === b[index]);
}
