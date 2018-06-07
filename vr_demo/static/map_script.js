// This example adds a search box to a map, using the Google Place Autocomplete
// feature. People can enter geographical searches. The search box will return a
// pick list containing a mix of places and predicted search terms.

// This example requires the Places library. Include the libraries=places
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places">
function is_URL(str){
   return (/^(http|https|ftp):\/\/[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$/i.test(str))
}

function initAutocomplete() {
    var map = new google.maps.Map(document.getElementById('map'), {
      center: {lat: -36.848836,lng: 174.76221},
      zoom: 13,
      mapTypeId: 'roadmap'
    });

    var geocoder = new google.maps.Geocoder();

    // Create the search box and link it to the UI element.
    var input = document.getElementById('pac-input');
    var searchBox = new google.maps.places.SearchBox(input);
    // Set initial restrict to the greater list of countries.
    //searchBox.setComponentRestrictions({'country': ['nz']});
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

    // Bias the SearchBox results towards current map's viewport.
    map.addListener('bounds_changed', function() {
      searchBox.setBounds(map.getBounds());
    });

    var markers = [];
    // Listen for the event fired when the user selects a prediction and retrieve
    // more details for that place.
    searchBox.addListener('places_changed', function() {
      //alert('places_changed')
      var places = searchBox.getPlaces();

      if (places.length == 0) {
        return;
      }

      // Clear out the old markers.
      markers.forEach(function(marker) {
        marker.setMap(null);
      });
      markers = [];

      // For each place, get the icon, name and location.
      var bounds = new google.maps.LatLngBounds();
      places.forEach(function(place) {
        if (!place.geometry) {
          console.log("Returned place contains no geometry");
          return;
        }

        image = "/static/images/rsz_green-home-icon2.png"
        var icon = {
          url: image,//place.icon,
//          size: new google.maps.Size(71, 71),
//          origin: new google.maps.Point(0, 0),
//          anchor: new google.maps.Point(17, 34),
//          scaledSize: new google.maps.Size(25, 25)
        };

        marker = new google.maps.Marker({
          map: map,
          icon: icon,
          title: place.name,
          position: place.geometry.location
        })

        marker.addListener('click', function() {
            geocoder.geocode( { 'location': marker.getPosition()}, function(results, status) {
                if (status == 'OK') {
                    var searchReq = $.get("/fetch_vr/" + results[0].formatted_address);
                    searchReq.done(function(url_address) { //todo data is valid vr address
                        if (is_URL(url_address)){
                            location.assign(url_address);
                        }
                        else {
//                            $('#upload').click();  //not working?
//                            var uploadReq = $.get("/upload");
                              location.assign("/upload")
                        }
                    });
                }
                else {
                    alert('Geocode was not successful for the following reason: ' + status);
                }
            });
        });

        // Create a marker for each place.
        markers.push(marker);

        if (place.geometry.viewport) {
          // Only geocodes have viewport.
          bounds.union(place.geometry.viewport);
        } else {
          bounds.extend(place.geometry.location);
        }
      });
      map.fitBounds(bounds);
    });
}