var mymap;
function init() {
  mymap = L.map('mapid').setView([46.4974, 11.3537], 11);

   L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
     '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
     'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: 'mapbox.streets'
   }).addTo(mymap);
   mymap.on("popupopen", function(e) { kkk = e;})
}

function add_bivacco(bivacco) {
  var marker = L.marker([bivacco.coordinate_x, bivacco.coordinate_y]).addTo(mymap);
  marker.bindPopup("<a href=\"viewbivacco/" + bivacco.id + "/"+'"' + "/>view in details</a>")
}

init();
