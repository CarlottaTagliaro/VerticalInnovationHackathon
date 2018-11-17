var mymap;
function init() {
  var h = window.innerHeight;
  var w = window.innerWidth;
  mymap = L.map('mapid').setView([46.4974, 11.3537], 11);

   L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
     '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
     'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: 'mapbox.streets'
   }).addTo(mymap);
   function resize() {
     document.getElementById("mapid").style.height = (h-56)+"px";
     document.getElementById("mapid").style.height = w+"px";
     window.mymap.invalidateSize()
   }
   setTimeout(resize(),300);
   window.onresize = function() {
     resize();
   };
   mymap.on("popupopen", function(e) { kkk = e;})
}

function add_bivacco(bivacco) {
  var marker = L.marker([bivacco.coordinate_x, bivacco.coordinate_y]).addTo(mymap);
  marker.bindPopup("<p>"+bivacco.name+"</p><a href=\"viewbivacco/" + bivacco.id + "/"+'"' + "/>view in details</a>")
}

init();
