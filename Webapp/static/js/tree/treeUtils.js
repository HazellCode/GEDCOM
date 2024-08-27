<!-- Utils -->
            function reloadpagewithgeneration(select) {
                var gen = select.value.split(" ")[1];


                var params = new URLSearchParams(location.search);
                params.set('generation',gen)
                window.location.search = params.toString();

            }
            function reloadpagewithid(id) {
                event.preventDefault()
                var params = new URLSearchParams(location.search);
                console.log("done")
                console.log(arguments.callee.caller.toString())
                params.set('indi',id)
                console.log(id)
                window.location.search = params.toString();


            }

            // 30-06-2022
            // I was adding error codes to the tree
            // They now are passing to the page and showing up in the console
            // You now need to display the content of the messages to the user in the div below
            // This div then needs to be converted to js so that it will only appear when there is an error
            // :)