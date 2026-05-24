
/**
* Create labels for every individual feature of a layer and add them to the map
* @param {mablibre-map} map - The maplibre map object
* @param {string} layerId - Name of the layer for which labels should be created
*/
export function createLabels(map, layerId){

    console.log('setting up labels...');
    const features = map.getSource('poi_source')._data.features;
    
    features.forEach(feature => {
        createLabel(feature, map);
    });

};


/**
* Create a single label for a single feature of a layer and add it to the map
* @param {mablibre-map} map - The maplibre map object
* @param {string} layerId - Name of the layer for which labels should be created
* @param {geojson-feature} feature - geographic feature
*/
function createLabel(feature, map) {

    console.log('creating labels');

    var popup = new maplibregl.Popup({
        className: 'popup',
        closeButton: false,
        closeOnClick: false,
        closeOnMove: false,
        offset: {
            'top': [0, 30],
            'bottom': [0, -30],
            'left': [30, 0],
            'right': [-30, 0]
        }
        });


    
    // get feature properties
    var name = feature.properties.name;
    var uri = feature.properties.URI;

    // combine into html-element
    const innerHTML = `
    <div class="riag-marker">
        <a href="${uri}" target="blank">
            <div class="riag_popup">
                <div class="riag_popup_content">
                    ${name}
                </div>
            </div>
        </a>
    </div>
    `;

    // calculate coordinates for popup
    const coords = feature.geometry.coordinates.slice();

    // create marker object
    popup.setLngLat(coords)
             .setHTML(innerHTML)
             .addTo(map);
};
