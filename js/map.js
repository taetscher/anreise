
import {addPOIs} from './layers/add_poi.js';
import { updateLabels } from './tooltips/update_labels.js';
import { createLabels } from './tooltips/labeling.js';

//create new map
const map = new maplibregl.Map({
            container: 'map',
            style: 'https://api.maptiler.com/maps/ch-swisstopo-lbm/style.json?key=9evOdBDbZ9ckseqCzPcE', // 100k free requests per Month
            hash: true, //set this to true when productive (shows xyz in URL and updates it on the fly)
            minZoom: 1,
            maxZoom: 19,
            center: [7.66704, 46.72928],
            zoom: 14.52
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

});

map.on('zoom', function(){
  updateLabels(map);
})