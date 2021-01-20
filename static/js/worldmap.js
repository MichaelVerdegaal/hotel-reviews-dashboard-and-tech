class ResetMeControl {
    insertControls() {
        this.container = document.createElement('div');
        this.container.classList.add('mapboxgl-ctrl');
        this.container.classList.add('mapboxgl-ctrl-group');
        this.container.classList.add('mapboxgl-ctrl-zoom');
        this.ResetMe = document.createElement('button');
        this.ResetMe.title = "Reset camera";
        this.ResetMe.setAttribute('type', 'button');
        this.ResetMe.style.backgroundImage = "url('https://upload.wikimedia.org/wikipedia/commons/f/f8/Ic_my_location_48px.svg')";
        this.ResetMe.style.backgroundSize = "29px 29px";
        this.ResetMe.style.backgroundRepeat = "no-repeat";
        this.container.appendChild(this.ResetMe);
    }

    onAdd(map) {
        this.map = map;
        this.insertControls();
        this.ResetMe.addEventListener('click', () => {
            this.map.flyTo({
                'center': [0, 50],
                'zoom': 4,
                'bearing': 0,
                'pitch': 0,
            });
        });
        return this.container;
    }

    onRemove() {
        this.container.parentNode.removeChild(this.container);
        this.map = undefined;
    }
}


function createMap(hotels) {
    let map = new mapboxgl.Map({
        container: 'map-container', // div to attach map to
        style: 'mapbox://styles/michaelverdegaal1999/ckiu3h1rq2ick19mhkkcxeymn', // stylesheet location
        center: [0, 50], // starting position [lng, lat]
        zoom: 4 // starting zoom
    });

    // Add map UI controls
    map.addControl(new mapboxgl.NavigationControl());
    map.addControl(new ResetMeControl());


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
                });

                map.addLayer({
                    id: 'map-point',
                    type: 'symbol',
                    source: 'points',
                    layout: {
                        'icon-image': 'custom-marker',
                        'icon-allow-overlap': true,
                        'icon-ignore-placement': true,
                        'icon-padding': 0,
                        'text-allow-overlap': true
                    }
                });
            }
        );

        // Center the map on clicked symbol, and show modal
        map.on('click', 'map-point', function (e) {
            let features = e.features[0];

            map.flyTo({
                'center': features.geometry.coordinates,
                'zoom': 18,
                'pitch': 70,
                'offset': [350, 0]
            });

            fillHotelModal(features.properties);
            $('#left_modal_xl').modal();
        });

        // Change the cursor to a pointer and show popup when hovering symbol
        // Reference: https://docs.mapbox.com/mapbox-gl-js/example/popup-on-hover/
        let popup = new mapboxgl.Popup({
            'closeButton': false,
            'closeOnClick': false,
            'offset': [0, -20]
        });

        map.on('mouseenter', 'map-point', function (e) {
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
        map.on('mouseleave', 'map-point', function () {
            map.getCanvas().style.cursor = '';
            popup.remove();
        });

        // Map filtering
        function filterBy(count, score) {
            let filterCount = ['>=', ['get', 'count'], count];
            let filterScore = ['>=', ['get', 'Average_Score'], score]
            map.setFilter('map-point', ['all', filterCount, filterScore]);
            document.getElementById('count-lbl').textContent = count;
            document.getElementById('review-lbl').textContent = score;
        }

        // Set initial values of slider
        filterBy(0, 0.0);

        // Call filter update on slider change
        document.getElementById('count-slider').addEventListener('input', function (e) {
            let month = parseInt(e.target.value, 10);
            let score = parseFloat(document.getElementById('review-lbl').innerText);
            filterBy(month, score);
        });
        document.getElementById('review-slider').addEventListener('input', function (e) {
            let month = parseInt(document.getElementById('count-lbl').innerText, 10);
            let score = parseFloat(e.target.value);
            filterBy(month, score);
        });

    });
}

function fillHotelModal(props) {
    let modal_content = document.getElementById("modal-body");
    modal_content.innerHTML = '';

    // Score badge next to modal title
    let score = props.Average_Score;
    let scoreBadgeContext = "";
    if (score >= 7) {
        scoreBadgeContext = "badge badge-success badge-secondary";
    } else {
        scoreBadgeContext = "badge badge-danger badge-secondary"
    }
    let scoreBadge = `<span class="${scoreBadgeContext}">${score}</span>`;

    // Modal title
    let modal_title = document.getElementById("modal-title");
    modal_title.innerHTML = props.Hotel_Name + scoreBadge;

    // Create review table
    let tableContainer = document.createElement("div");
    tableContainer.className = "container-fluid";
    tableContainer.id = "table-container";

    let reviewTable = document.createElement("table");
    reviewTable.className = "table table-striped table-hover";
    reviewTable.id = "review-table";

    tableContainer.appendChild(reviewTable);
    tableContainer.appendChild(document.createElement("th"));
    modal_content.appendChild(tableContainer);

    // Fill review table
    let endpoint = `/hotel/${props.Hotel_Name}`;
    $("#review-table").DataTable({
        ajax: {
            url: endpoint,
            dataType: "json",
            dataSrc: "",
            contentType: "application/json; charset=utf-8",
        },
        columns: [
            {'title': 'Date', 'data': 'Review_Date'},
            {'title': 'Review', 'data': 'Review'},
            {'title': 'Country', 'data': 'Reviewer_Nationality'},
            {'title': 'Score', 'data': 'Reviewer_Score'},
            {'title': 'Sentiment', 'data': 'Sentiment'},
        ],
    });
}

function fillSentimentModal() {
    $('#sentiment_modal').modal();
    $('#raw-review-btn').click(function () {
        let reviewText = $('#raw-review').val();
        reviewText = reviewText.replace(/\//g, "")
        if (reviewText.length >= 1990) {
            reviewText = reviewText.substring(0, 1990);
        }
        let endpoint = `/judge/${reviewText}`;
        $.ajax({
            url: endpoint,
            contentType: 'application/json',
            dataType: 'json',
            success: function (result) {
                let rnn_conf = (result['RNN'][0]).toFixed(5);
                let rnn_pred = result['RNN'][1];
                let lstm_conf = (result['LSTM'][0]).toFixed(5);
                let lstm_pred = result['LSTM'][1];
                let gru_conf = (result['GRU'][0]).toFixed(5);
                let gru_pred = result['GRU'][1];

                $('#rnn_conf').text(`Confidence in this choice: ${rnn_conf}`);
                $('#rnn_pred').text(`Your text has a ${rnn_pred} sentiment`);
                $('#lstm_conf').text(`Confidence in this choice: ${lstm_conf}`);
                $('#lstm_pred').text(`Your text has a ${lstm_pred} sentiment`);
                $('#gru_conf').text(`Confidence in this choice: ${gru_conf}`);
                $('#gru_pred').text(`Your text has a ${gru_pred} sentiment`);

                if (rnn_pred === "Positive") {
                    $('div#rnn-body').css("background-color", "lightgreen");
                } else {
                    $('div#rnn-body').css("background-color", "indianred");
                }
                if (lstm_pred === "Positive") {
                    $('div#lstm-body').css("background-color", "lightgreen");
                } else {
                    $('div#lstm-body').css("background-color", "indianred");
                }
                if (gru_pred === "Positive") {
                    $('div#gru-body').css("background-color", "lightgreen");
                } else {
                    $('div#gru-body').css("background-color", "indianred");
                }
            }
        });
    });
}