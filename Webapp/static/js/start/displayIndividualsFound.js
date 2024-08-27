// now we have the tree we can   the auto complete logic.
const indexsearch = document.getElementById('index-search')
const indexmatchList = document.getElementById('index-list')




function makeIndexList(text){
    let allindi = JSON.parse(window.localStorage['allindi'])
  var indexnames = []

  for (person in allindi) {

      if (allindi[person].surname.length !== typeof(int)){

      }
      if (allindi[person].name == ""){

      } else if ((allindi[person].name.join(" ").toUpperCase() + allindi[person].surname.join(" ").toUpperCase()).includes(text.toUpperCase())) {
        indexnames.push([allindi[person].id,allindi[person].name.join(" "),allindi[person].surname,allindi[person].born])
      }


  }

    if (text.length === 0) {

        text = " ";

    }

    indexnames.sort((a,b) => a[1].localeCompare(b[1]))

  if (indexnames.length > 0 ){

    const card = indexnames.map(indi => `
      <button class="list-group-item li" onclick="window.localStorage.setItem('rootindi','${indi[0]}');">${indi[1]} <b>${indi[2]}</b> <span class="index-list-card-born"> - ${indi[3]}</span></button>
      
      
    `).join('');

    indexmatchList.innerHTML = card
      $(".li").hover(function () {
                //toggleClass() switches the active class
                $(this).toggleClass("index-highlighted");
            });
      $(".li").click(function() {
          $(this).parent().find('.li.selected').removeClass('selected')
          $(this).addClass('selected')
      })
  } else {
      indexnames = []
        indexmatchList.innerHTML = ""

  }
}

// We need to add an event listener to the actual button so that it can update the text on the sidebar
const indexnameview = document.getElementById('index-name-view')
const indexidview = document.getElementById('index-id-view')
indexmatchList.addEventListener('click',function(evt){


    indexnameview.textContent = "Name: " + evt.target.textContent.split("-")[0]
    indexidview.textContent = "ID: " + window.localStorage.getItem('rootindi')
})

indexsearch.addEventListener('input',() => makeIndexList(indexsearch.value));

