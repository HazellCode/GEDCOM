// given the tree from localstorage return the individual object

function getDatafromID(id){

    function reccur(id,node){
    if (tree.id === id) {
        return tree
    } else {
        for (par in tree.parents){
            reccur(id,tree.parents[par])
        }
    }

    }
    return reccur(id,0)
}


