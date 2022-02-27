function initMap() {
	const latitude = parseFloat(lat);
	const longitude = parseFloat(lng);
	const directionsRenderer = new google.maps.DirectionsRenderer();
	const directionsService = new google.maps.DirectionsService();
	const map = new google.maps.Map(document.getElementById("map"), {
		zoom: 7,
		center: { lat: latitude, lng: longitude },
		disableDefaultUI: true,
	});
	const marker = new google.maps.Marker({
		position: { lat: latitude, lng: longitude },
		map: map,
	});

	directionsRenderer.setMap(map);
	directionsRenderer.setPanel(document.getElementById("sidebar"));

	const control = document.getElementById("floating-panel");

	map.controls[google.maps.ControlPosition.TOP_CENTER].push(control);

	const onChangeHandler = function () {
		calculateAndDisplayRoute(directionsService, directionsRenderer);
	};

	document.getElementById("start").addEventListener("change", onChangeHandler);
	// document.getElementById("end").addEventListener("change", onChangeHandler);
}

function calculateAndDisplayRoute(directionsService, directionsRenderer) {
	const start = document.getElementById("start").value;
	// const end = document.getElementById("end").value;

	directionsService
		.route({
			origin: start,
			destination: end,
			travelMode: google.maps.TravelMode.DRIVING,
		})
		.then((response) => {
			directionsRenderer.setDirections(response);
		})
		.catch((e) => window.alert("Directions request failed due to " + status));
}

const fav_btn = document.querySelector(".business__add__fav");
fav_btn.addEventListener("click", () => {
	fav_btn.textContent = "Added to Favorites!";
});
