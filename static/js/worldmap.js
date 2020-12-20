function createMap(hotels) {
    let map = new mapboxgl.Map({
        container: 'map-container', // div to attach map to
        style: 'mapbox://styles/michaelverdegaal1999/ckiu3h1rq2ick19mhkkcxeymn', // stylesheet location
        center: [0, 50], // starting position [lng, lat]
        zoom: 4 // starting zoom
    });

    // Add map UI controls
    map.addControl(new mapboxgl.NavigationControl());

    // Add markers
    map.on('load', function () {
        // Add an image to use as a custom marker
        map.loadImage(
            'https://docs.mapbox.com/mapbox-gl-js/assets/custom_marker.png',
            function (error, image) {
                if (error) throw error;
                // Add symbol image (currently mapbox default)
                map.addImage('custom-marker', image);
                // Add data source
                map.addSource('points', {
                    'type': 'geojson',
                    'data': hotels,
                    'cluster': true,
                    'clusterMaxZoom': 12, // Max zoom to cluster points on
                    'clusterRadius': 50 // Radius of each cluster when clustering points (defaults to 50)
                });

                // Clustering reference: https://docs.mapbox.com/mapbox-gl-js/example/cluster/
                map.addLayer({
                    id: 'clusters',
                    type: 'circle',
                    source: 'points',
                    filter: ['has', 'point_count'],
                    paint: {
                        // Uses step expressions (https://docs.mapbox.com/mapbox-gl-js/style-spec/#expressions-step)
                        // to implement three types of circles:
                        'circle-color': [
                            'step',
                            ['get', 'point_count'],
                            '#4ea9ee',
                            50,
                            '#9759f7',
                            300,
                            '#ea688c'
                        ],
                        'circle-radius': [
                            'step',
                            ['get', 'point_count'],
                            20,
                            50,
                            30,
                            300,
                            40
                        ]
                    }
                });

                map.addLayer({
                    id: 'cluster-count',
                    type: 'symbol',
                    source: 'points',
                    filter: ['has', 'point_count'],
                    layout: {
                        'text-field': '{point_count_abbreviated}',
                        'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Bold'],
                        'text-size': 12
                    }
                });

                map.addLayer({
                    id: 'unclustered-point',
                    type: 'symbol',
                    source: 'points',
                    layout: {
                        'icon-image': 'custom-marker'
                    },
                    filter: ['!', ['has', 'point_count']],
                });

                // inspect a cluster on click
                map.on('click', 'clusters', function (e) {
                    let features = map.queryRenderedFeatures(e.point, {
                        layers: ['clusters']
                    });
                    let clusterId = features[0].properties.cluster_id;
                    map.getSource('points').getClusterExpansionZoom(
                        clusterId,
                        function (err, zoom) {
                            if (err) return;
                            map.easeTo({
                                center: features[0].geometry.coordinates,
                                zoom: zoom
                            });
                        }
                    );
                });
            }
        );

        // Center the map on clicked symbol, and show modal
        map.on('click', 'unclustered-point', function (e) {
            let features = e.features[0];

            map.flyTo({
                'center': features.geometry.coordinates,
                'zoom': 18,
                'pitch': 70,
                'offset': [200, 0]
            });

            fillHotelModal(features.properties);
            $('#left_modal').modal();
        });

        // Change the cursor to a pointer and show popup when hovering symbol
        // Reference: https://docs.mapbox.com/mapbox-gl-js/example/popup-on-hover/
        let popup = new mapboxgl.Popup({
            'closeButton': false,
            'closeOnClick': false,
            'offset': [0, -20]
        });
        map.on('mouseenter', 'unclustered-point', function (e) {
            map.getCanvas().style.cursor = 'pointer';
            let features = e.features[0]
            let props = features.properties

            let coordinates = features.geometry.coordinates.slice();
            let description = `<h6>${props.Hotel_Name}</h6><p>
                                📍 Address: ${props.Hotel_Address}<br>
                                7️⃣ Average score: ${props.Average_Score}<br>
                                💬 Reviews: ${props.count}</p>`

            // Ensure that if the map is zoomed out such that multiple
            // copies are visible, the popup moves to the copy
            while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
                coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
            }

            // Populate the popup and set its coordinates
            popup.setLngLat(coordinates).setHTML(description).addTo(map);
        });

        // Revert cursor style andd remove popup when not hovering symbol anymore
        map.on('mouseleave', 'unclustered-point', function () {
            map.getCanvas().style.cursor = '';
            popup.remove();
        });
    });
}

function fillHotelModal(props) {
    let modal_content = document.getElementById("modal-body");
    let modal_title = document.getElementById("modal-title");
    modal_content.innerHTML = '';

    let score = props.Average_Score;
    let scoreBadgeContext = "";

    if (score >= 7) {
        scoreBadgeContext = "badge badge-success badge-secondary";
    } else {
        scoreBadgeContext = "badge badge-danger badge-secondary"
    }
    let scoreBadge = `<span class="${scoreBadgeContext}">${score}</span>`;
    modal_title.innerHTML = props.Hotel_Name + scoreBadge;
}