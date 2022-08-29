
document.addEventListener('alpine:init', () => {


    Alpine.data('form_data', () => ({
        url: "",

        start_analyse(){
            let url = this.url;

            fetch("/analyse",
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({"url":url})
                }
            ).then(res => window.location="/result.html")
        }
    }))  





})