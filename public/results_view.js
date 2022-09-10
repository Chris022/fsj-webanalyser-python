function init() {
    return {
        "request_urls": [],
        "request_list": [],
        "cookie_urls": [],
        "cookie_list": [],
        "visited_urls":[],
        "visited_url_data": function () {
            get_analyse_results().then(results => results["list_of_visited_urls"]).then(results => {
                this.visited_urls = results;
            })
        },
        "thrid_party_data": function () {

            get_analyse_results().then(results => results["analyse_results"]).then(results => {
                let request_list = [];
                let request_urls = {};

                Object.keys(results).forEach((url) => {
                    let requests = results[url]["third-party-requests"];

                    requests.forEach(request => {
                        let id = null;
                        if (!request_list.includes(request)) {
                            id = request_list.length;
                            request_list.push(request);
                        } else {
                            id = request_list.findIndex(el => el == request)
                        }

                        if (request_urls[id]) request_urls[id].push(url)
                        else request_urls[id] = [url]
                    })

                })

                //add id to cookies 
                request_list = request_list.map((request, index) => { return { "id": index, "request": request } })

                this.request_list = request_list;
                this.request_urls = request_urls;
            })
        },
        "cookie_data": function () {
            //go through every url and collect thrid party cookies
            /**
             * 
             * [cookie]
             * 
             * {
             *      cookie_index:[list of urls]
             * 
             * }
             * 
             */
            get_analyse_results().then(results => results["analyse_results"]).then(results => {
                let cookie_urls = {};
                let cookie_list = [];

                Object.keys(results).forEach((url) => {
                    let cookies = results[url]["cookies"];

                    cookies = cookies.map(cookie => {
                        return {
                            "name": cookie["name"],
                            "domain": cookie["domain"]
                        }
                    });

                    cookies.forEach(cookie => {
                        let id = null;
                        if (!cookie_list.map(cookie => JSON.stringify(cookie)).includes(JSON.stringify(cookie))) {
                            id = cookie_list.length;
                            cookie_list.push(cookie);
                        } else {
                            id = cookie_list.findIndex(el => JSON.stringify(el) == JSON.stringify(cookie))
                        }

                        if (cookie_urls[id]) cookie_urls[id].push(url)
                        else cookie_urls[id] = [url]
                    })

                })

                //add id to cookies 
                cookie_list = cookie_list.map((cookie, index) => { return { "id": index, ...cookie } })

                this.cookie_list = cookie_list;
                this.cookie_urls = cookie_urls;
            })
        }

    }
}


async function get_analyse_results() {
    
    let urlParams = new URLSearchParams(window.location.search);
    let url = urlParams.get('url')

    const response = await fetch("/results", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "url": url }) // body data type must match "Content-Type" header
    }).then(result => result.json());

    if (response.type == "SUCCESS") {
        return response.data;
    }
    alert("Sorry... Something unexpected happend!");
    window.location="/";
}