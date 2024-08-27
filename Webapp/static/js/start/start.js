
//
//  Author: Archie
//  Date: 5/09/2022
//  File Name: start.js
//  Description: Takes the file input from the user and send it to the python script for it to be parsed,
//  Then gets a status code back from the python script and using that will either redirect the user to
//  the pick user dialog or display an error
//


var submitButton = document.getElementById("submit-file-button")


submitButton.onclick = function(){
    var ged = document.getElementById("fileinput").files[0];
    let ged_data;
    if (ged) {
        ged_data = ""
        var read = new FileReader()
        read.readAsText(ged, "UTF-8")
        read.onload = function (e) {
            console.log("Success")
            // Now that we have the data in the file we need to send it to the python script for it to be parsed.

            fetch("/api/userGED",{
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({"data":e.target.result})

            })
                .then(res => res.json())
                .then(data => {
                    // If there were no errors and the file was parsed correctly we can now redirect the user to the select user page
                    if (data['status'] === 0){
                        // The process was a success the file has been parsed and we can now redirect the user
                        window.location.href = "/start"
                    }
                })



            ged_data = e.target.result;
        }
        read.onerror = function (e) {
            ged_data = "Error"
        }

    }






};


