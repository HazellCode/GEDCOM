async function openDB(){
    return await idb.openDB("tree_data", 1, {
        upgrade(db, oldVersion, newVersion, transaction) {
            console.log("Upgraded DB")
            if (!db.objectStoreNames.contains('individuals')) {
                var idb_tree_data_indi = db.createObjectStore('individuals', {keyPath: 'id'});
                idb_tree_data_indi.createIndex('id', 'id', {unique: true});
                idb_tree_data_indi.createIndex('generation','generation',{unique: false})
            }
            if (!db.objectStoreNames.contains('individual_detail')) {
                var idb_indi_detail = db.createObjectStore('individual_detail', {keyPath: 'ID'});
                idb_indi_detail.createIndex('ID', 'ID', {unique: true});

            }




        },
        terminated(){
            console.log("there was an error")
        },


    });

}





async function deleteDB(){
    return await idb.deleteDB("tree_data",{
        blocked() {
            console.log("Unable to delete db")
        },

    }).then(function(){
        console.log("DB deleted")
    })
}


async function clearDBStore(dbprom){
    dbprom.then(function (db){
        var tx = db.transaction('individuals','readwrite');
        var store = tx.objectStore('individuals')
        store.clear()
    })
}


// ok so what we are going to do is store the individuals seperately with their id's

async function storeIndi(dbprom,individual){

    dbprom.then(function (db){
        var tx = db.transaction('individuals','readwrite');
        var store = tx.objectStore('individuals')
        store.clear()
        console.log(individual)
        for (indi in individual){
            console.log(indi)
            store.add(individual[indi]);
        }


        return tx.done;


    }).catch(function(err){
        if (err.message === "AbortError"){
            console.log("This individual already exists in the Database")
        }
    })

}

async function storeDetail(dbprom,individual){

    dbprom.then(function (db){
        var tx = db.transaction('individual_detail','readwrite');
        var store = tx.objectStore('individual_detail')
        store.clear();

        console.log(individual)
        store.add(individual);



        return tx.done;


    }).catch(function(err){
        if (err.message === "AbortError"){
            console.log("This individual already exists in the Database")
        }
    })

}


async function storeIndiUUID(dbprom, uuid){
    dbprom.then(function (db){
        var tx = db.transaction('individuals','readwrite');
        var store = tx.objectStore('individuals')



        store.add(uuid);



        return tx.done;


    }).catch(function(err){
        if (err.message === "AbortError"){
            console.log("[uuid]error")
        }
    })
}












var dbprom = openDB()