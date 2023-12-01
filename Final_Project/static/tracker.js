let map;
let marker;

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 0, lng: 0 },
        zoom: 8,
    });

    // Set up a dummy marker
    marker = new google.maps.Marker({
        map: map,
        title: 'Current Location',
    });
}

function updateLocation(latitude, longitude) {
    const location = new google.maps.LatLng(latitude, longitude);
    map.setCenter(location);
    marker.setPosition(location);
}

// Simulate real-time updates (replace with actual server updates)
setInterval(() => {
    const newLatitude = Math.random() * 10; // Replace with actual latitude
    const newLongitude = Math.random() * 10; // Replace with actual longitude
    updateLocation(newLatitude, newLongitude);
    console.log(`Updated Location: ${newLatitude}, ${newLongitude}`);
}, 5000); // Update every 5 seconds
