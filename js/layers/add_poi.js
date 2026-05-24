import { loadIcons } from '../icons/load_icons.js';

export async function addPOIs(map) {
    /**
    *Add source, layer and user interaction of poi to map
    *@param  {mapbox map object}   map   The map which receives the poi layer
    */

    // add images for styling
    await loadIcons(map);

    const response = await fetch('./geojson/poi.geojson'); // Or your API URL
    const geojsonData = await response.json();
    
    //in order to use data with mapbox, you need to add a source first
    map.addSource('poi_source', {
            type: 'geojson',
            data: geojsonData,
            attribution: "© melyamin",
            //cluster: true,
            //clusterMaxZoom: 7,
            //clusterRadius: 50
        })
    
    //add the layer
    map.addLayer({
        id: 'pois',
        type: 'symbol',
        source: 'poi_source',
        maxzoom: 20,
        layout: {
            'icon-image': ['concat', 'custom_', ['get', 'kind']],
            'icon-size': ['get', 'icon_size'],
            'icon-overlap': "never",
            'symbol-sort-key': [
                'match', ['get', 'kind'],
                'castle', 0,
                'no_parking', 1,
                'parking', 2,
                'bus', 3,
                'restaurant', 4
                , 8
            ]
        }
        });

    // add mousepointer handling
    // Change the cursor to a pointer when the mouse is over the affected layer.
    map.on('mouseenter', 'pois', () => {
        map.getCanvas().style.cursor = 'pointer';
    });

    // Change it back to a pointer when it leaves.
    map.on('mouseleave', 'pois', () => {
        map.getCanvas().style.cursor = '';
    });

    map.on('click', 'pois', (e) => {
        const feature = e.features[0];

        map.getCanvas().style.cursor = 'pointer';

        const coordinates = feature.geometry.coordinates.slice();
        const targetCenter = [coordinates[0], coordinates[1]];

        map.flyTo({
            center: targetCenter,
            zoom: 17,
            speed: 1.2,
            essential: true
        });
    });

    console.log('pois added.')
    
};
