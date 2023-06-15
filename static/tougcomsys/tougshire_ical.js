// if (!$) {
//     // Need this line because Django also provided jQuery and namespaced as django.jQuery
//     $ = django.jQuery;
// }

window.onload = function() {
    document.getElementById('id_ical').onchange = function(e) {
        document.getElementById('id_ical_text').innerText=e.target.value
    }
}