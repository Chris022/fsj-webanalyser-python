function analyse_view_init(){
    
    return {
        url: "",
        start_analyse: function (){
            fetch("/analyse", {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify({"url":this.url})
            }).then(()=>{window.location="/loading_view.html?url="+this.url});
        }
    }
}
