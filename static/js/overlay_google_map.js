function overlayCanvasonGoogleMap(xllcorner,xurcorner,yllcorner,yurcorner)
{
  
  var rectLatLngCenter = new google.maps.LatLng((yurcorner+yllcorner)/2, (xurcorner+xllcorner)/2);

  overlayImageOnMap();


  function initialize() {

    imageBounds = {
      // north is bigger than south, east is bigger than west
      north: yurcorner,
      south: yllcorner,
      east: xurcorner,
      west: xllcorner
    };


    var mapOptions = {
      zoom: 12,
      center: rectLatLngCenter,
      mapTypeId: google.maps.MapTypeId.SATELLITE
    };

    map = new google.maps.Map(document.getElementById('googleMapDiv'),
        mapOptions);

    imgOverlay = new google.maps.GroundOverlay(
        imgURL,
        imageBounds);

    imgOverlay.setMap(map);
    // set transparency
    imgOverlay.setOpacity(0.5);
  }


  function overlayImageOnMap()
  {
    // should create map when myCanvas is fully done
    html2canvas(document.getElementById("myCanvas"), 
      {
        onrendered: function(canvas) {
          imgURL = canvas.toDataURL();
          google.maps.event.addDomListener(window, 'load', initialize);
          imgOverlay.setOpacity(0.5);
        }
      }); 
  }

}

// add the overlay on google map
function addOverlay() {  
  imgOverlay.setMap(map);
}

// remove the overlay on google map
function removeOverlay() {
  imgOverlay.setMap(null);
}

function updateMapOverlay()
{
  imgOverlay.setMap(null);
  // add a new overlay
  imgURL = document.getElementById("myCanvas").toDataURL();

  imgOverlay = new google.maps.GroundOverlay(
    imgURL,
    imageBounds);
  imgOverlay.setMap(map);
}

function changeOverlayOpacity()
{
  var opacityStr = document.getElementById('opacitySelectorID').value;
  imgOverlay.setOpacity(parseFloat(opacityStr));
}
