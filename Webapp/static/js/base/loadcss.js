// take in the html filename and return load the css for it.
// Make sure that the theme variable exists in localStorage
    if (!localStorage['theme']) {
        localStorage['theme'] = 'lightmode'
    }

    // we need to get the path of the page so that we can load the css for de page
    var pagename = window.location.pathname.split("/").pop();
   // Loads the correct css depending on the data stored in localstorage
    var cssHEAD = document.getElementsByTagName('HEAD')[0];
    var cssLIST = []
if (pagename === "start") {
    // I need to have a system that loads css from a list of css due to every page requiring base css for the navbar

    if (localStorage['theme'] === "darkmode"){
        cssLIST = ["darkmode-base.css","darkmode-index.css"]
    } else {
        cssLIST = ["base.css","index.css","footer.css"]
    }
} else if (pagename === "tree"){

    if (localStorage['theme'] === "darkmode"){
        cssLIST = ["darkmode-tree.css","darkmode-base.css"]

    } else {
        cssLIST = ["tree.css","base.css"]

    }
} else if (pagename === "error"){
    if (localStorage['theme'] === "darkmode"){
        cssLIST = ["darkmode-error.css","darkmode-base.css"]

    } else {
        cssLIST = ["error.css","base.css"]

    }
} else if (pagename === "profile"){
    if (localStorage['theme'] === "darkmode"){
        cssLIST = ["darkmode-profile.css","darkmode-base.css","darkmode-footer.css"]

    } else {
        cssLIST = ["profile.css","base.css","footer.css"]

    }

} else if (pagename === ""){
    if (localStorage['theme'] === "darkmode"){
        cssLIST = ["darkmode-start.css","darkmode-base.css"]

    } else {
        cssLIST = ["start.css","base.css","footer.css"]

    }
} else if (pagename === "file_stats"){
    if (localStorage['theme'] === "darkmode"){
        cssLIST = ["darkmode-file_stats.css","darkmode-base.css"]

    } else {
        cssLIST = ["file_stats.css","base.css","footer.css"]

    }
}

if (cssLIST.length === 0) {
     if (localStorage['theme'] === "darkmode"){
        cssLIST = ["darkmode-base.css"]

    } else {
        cssLIST = ["base.css"]

    }

}

for (link in cssLIST){
    var cssLINK = document.createElement('link')
    cssLINK.rel = "stylesheet"
    cssLINK.type = "text/css"
    cssLINK.href = "../static/css/" + localStorage['theme'] + "/" + cssLIST[link]
    cssLINK.id = cssLIST[link]
    cssHEAD.appendChild(cssLINK)
}







