

// now we have the tree we can start the auto complete logic.
const search = document.getElementById('indi-search')
const matchList = document.getElementById('match-list')



function makeList(text){
  var names = []

  for (person in allindi) {
      if ((allindi[person].name.join(" ").toUpperCase() + allindi[person].surname.toUpperCase()).includes(text.toUpperCase())) {
        names.push([allindi[person].id,allindi[person].name.join(" "),allindi[person].surname])
      }


  }

    if (text.length === 0) {
        names = []
        matchList.innerHTML = ""

    }
    console.log(names)
    names.sort((a,b) => a[1].localeCompare(b[1]))

  if (names.length > 0 ){
    const card = names.map(indi => `
      <button id="${indi[0]}"class="list-group-item li">${indi[1]} <b>${indi[2]}</b></button>
      
    `).join('');

    matchList.innerHTML = card
      $(".li").hover(function () {
                //toggleClass() switches the active class
                $(this).toggleClass("highlighted");
            });
      $('.li').click(function(evt){
          console.log(evt.target.id)
          window.localStorage['tempID'] = event.target.id
          reloadpagewithid(evt.target.id)

      })


  } else {
      names = []
        matchList.innerHTML = ""

  }
}

// Filter the users and display those that match


search.addEventListener('input',() => makeList(search.value));

