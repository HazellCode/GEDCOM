 fetch("/api/file_stats",{
                method: "GET",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: null

            })
                .then(res => res.json())
                .then(data => {
                    console.log(data)
                })