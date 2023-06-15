
window.onload = function() {
    document.getElementById('id_ical').onchange = function(e) {
        const xhttp = new XMLHttpRequest();
        ical_text_url = document.getElementById('id_ical_text_url').innerText

        xhttp.onload = function() {
            response_text = this.responseText.replaceAll('BEGIN:VEVENT', '\nBEGIN:VEVENT')
            document.getElementById('id_ical_text').innerHTML = '<pre>' + response_text + '</pre>';
        }

        if( document.getElementById('id_ical').value )
            ical_text_url = ical_text_url.replace('/0/', '/' + document.getElementById('id_ical').value + '/' )

        xhttp.open("GET", ical_text_url, true) ;
        xhttp.send();   
    }
}