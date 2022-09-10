async function loading_view_init(){
    handle_status()
    setInterval(() => {
        handle_status()
    }, 5000);
}

async function handle_status(){
    let urlParams = new URLSearchParams(window.location.search);
    let url = urlParams.get('url')

    let status = await check_analysing_status();

    if(status == "not_analysed"){
        alert("Wohaaa... That url is not analysed yet. Please first analyse it!");
        window.location="/analyse_view.html";
    }
    if(status == "still_analysing"){
        //do nothing
    }
    if(status == "finished_analysing"){
        window.location="/results_view.html?url="+url;
    }
}

async function check_analysing_status(){

    let urlParams = new URLSearchParams(window.location.search);
    let url = urlParams.get('url')

    const response = await fetch("/results", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({"url":url}) // body data type must match "Content-Type" header
    }).then(result => result.json());

    if(response.type=="SUCCESS"){
        return "finished_analysing";
    }
    if(response.data == "not_analysed"){
        return "not_analysed";
    }
    if(response.data == "still_analysing"){
        return "still_analysing";
    }
    return "other_error";
}