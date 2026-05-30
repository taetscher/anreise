
import {addPOIs} from './layers/add_poi.js';
import { updateLabels } from './tooltips/update_labels.js';
import { createLabels } from './tooltips/labeling.js';
import { createCountdown } from './countdown.js';

//create new map
const map = new maplibregl.Map({
            container: 'map',
            style: 'https://api.maptiler.com/maps/019e7877-7fcb-73b3-9af2-783221b0b645/style.json?key=9evOdBDbZ9ckseqCzPcE', // 100k free requests per Month
            hash: true, //set this to true when productive (shows xyz in URL and updates it on the fly)
            minZoom: 1,
            maxZoom: 19,
            center: [7.65309,46.742],
            zoom: 11.8
            //,preserveDrawingBuffer: true
          });

//add map controls
map.addControl(new maplibregl.NavigationControl());
map.addControl(new maplibregl.ScaleControl({position: "bottom-left"}))

//when map is loaded, load additional layers
map.on('load', async function() {
    
    //addTravels(map);
    await addPOIs(map);
    createLabels(map, 'pois');
    updateLabels(map);
    createCountdown("June 19, 2026 13:00:00")

});

map.on('zoom', function(){
  updateLabels(map);
})