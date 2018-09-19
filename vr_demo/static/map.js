        var icon = {
            url:"/static/images/streetview.png",
        };
        var marker;

        function get_para(vars) {
           return vars
        }

        function clickMarker(marker,place_id){
            if(marker){
                <!--location.assign("/fetch_vr/" + place_id);-->
//                console.log(marker.title);
                location.assign("/matterport/" + marker.title);
            }else{
                alert("no valid marker")
            }
        }

        function placeMarkerAndPanTo(latLng, map) {
            var marker = new google.maps.Marker({
                position: latLng,
                map: map,
                icon:icon
            });
            var geocoder= new google.maps.Geocoder();
            geocoder.geocode( { 'location': marker.getPosition()}, function(results, status) {
                if (status == 'OK') {
                    place_id = JSON.stringify(results[0]["place_id"]);
                    place_id = place_id.replace(/^"(.*)"$/, '$1');
                    marker.addListener('click', function(){clickMarker(marker,place_id)});
                }else {
                    alert('Geocode was not successful for the following reason: ' + status);
                }
            });
        }

        function showLocationButton(map, marker)
        {
            var controlDiv = document.createElement('div');

            var firstChild = document.createElement('button');
            firstChild.style.backgroundColor = '#fff';
            firstChild.style.border = 'none';
            firstChild.style.outline = 'none';
            firstChild.style.width = '40px';
            firstChild.style.height = '40px';
            firstChild.style.borderRadius = '2px';
            firstChild.style.boxShadow = '0 1px 4px rgba(0,0,0,0.3)';
            firstChild.style.cursor = 'pointer';
            firstChild.style.marginRight = '10px';
            firstChild.style.padding = '0px';
            firstChild.title = 'Your Location';
            controlDiv.appendChild(firstChild);

            var secondChild = document.createElement('div');
            secondChild.style.margin = '11px';
            secondChild.style.width = '18px';
            secondChild.style.height = '18px';
            secondChild.style.backgroundImage = 'url(https://maps.gstatic.com/tactile/mylocation/mylocation-sprite-1x.png)';
            secondChild.style.backgroundSize = '180px 18px';
            secondChild.style.backgroundPosition = '0px 0px';
            secondChild.style.backgroundRepeat = 'no-repeat';
            secondChild.id = 'you_location_img';
            firstChild.appendChild(secondChild);

            google.maps.event.addListener(map, 'dragend', function() {
                $('#you_location_img').css('background-position', '0px 0px');
            });

            firstChild.addEventListener('click', function() {
                var imgX = '0';
                var animationInterval = setInterval(function(){
                    if(imgX == '-18') imgX = '0';
                    else imgX = '-18';
                    $('#you_location_img').css('background-position', imgX+'px 0px');
                }, 500);
                if(navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(function(position) {
                        var latlng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
//                        marker.setPosition(latlng);
                        map.setCenter(latlng);
                        clearInterval(animationInterval);
                        $('#you_location_img').css('background-position', '-144px 0px');
                    });
                }
                else{
                    clearInterval(animationInterval);
                    $('#you_location_img').css('background-position', '0px 0px');
                }
            });

            controlDiv.index = 1;
            map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(controlDiv);
        }


        function initAutocomplete(){
            loc = get_para(locationString);
            place_id = loc.place_id;
            lat = parseFloat(loc.lat);
            lng = parseFloat(loc.lng);
//            alert("lat:"+lat+"lng:"+lng);
            var map = new google.maps.Map(document.getElementById('map'), {
                center: {lat: lat,lng: lng},
                zoom: 13,
                mapTypeId: 'roadmap',
                disableDoubleClickZoom : true,
                fullscreenControl: false,
                mapTypeControl: false,
            });

            var markers = [];
            // Create the search box and link it to the UI element.
            var input = document.getElementById('pac-input');
            var searchBox = new google.maps.places.SearchBox(input);
//            map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

            // Bias the SearchBox results towards current map's viewport.
            map.addListener('bounds_changed', function() {
                searchBox.setBounds(map.getBounds());
            });

            latlng = new google.maps.LatLng(lat, lng);
//            marker = new google.maps.Marker({map: map,icon: icon,title: place_id,position: latlng});
            latlng1 = new google.maps.LatLng(-36.8821759, 174.77358950000007);
            marker1 = new google.maps.Marker({map: map,title: "16 Bracken Ave",position: latlng1});

            markers.push(marker1)
            latlng2 = new google.maps.LatLng(-36.9077891,174.81203219999998);
            marker2 = new google.maps.Marker({map: map,title: "Flua Lighting",position: latlng2});
//            marker2 = new google.maps.Marker({map: map,icon: icon,title: "Flua Lighting",position: latlng2});

            markers.push(marker2)
            marker1.addListener('click', function(){clickMarker(marker1,place_id)})
            marker2.addListener('click', function(){clickMarker(marker2,place_id)})

            map.addListener('dblclick', function(e) {
                marker.setMap(null);
//                placeMarkerAndPanTo(e.latLng, map);
                e.stop();
            });

            showLocationButton(map, marker);

            // Listen for the event fired when the user selects a prediction and retrieve
            // more details for that place.
            searchBox.addListener('places_changed', function() {
              var places = searchBox.getPlaces();

              if (places.length == 0) {
                return;
              }

              // Clear out the old markers.
//              markers.forEach(function(marker) {
//                marker.setMap(null);
//              });
//              markers = [];

              // For each place, get the icon, name and location.
              var bounds = new google.maps.LatLngBounds();
              places.forEach(function(place) {
                if (!place.geometry) {
                  console.log("Returned place contains no geometry");
                  return;
                }

//                // Create a marker for each place.
//                marker = new google.maps.Marker({
//                  map: map,
//                  icon: icon,
//                  title: place.name,
//                  position: place.geometry.location
//                })

                console.log("lat:"+ place.geometry.location.lat()+" lng:"+place.geometry.location.lng());
                console.log(place.name);

//                marker.addListener('click', function(){clickMarker(marker,place.place_id)})
//                markers.push(marker);

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