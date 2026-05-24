/**
* Update existing labels (hide/show on zoom)
* @param {mablibre-map} map - The maplibre map object
*/
export function updateLabels(map) {
  // get current zoom level and determine if labels should show or not
  const zoom = map.getZoom();
  const visible = zoom >= 16 ? 'flex' : 'none';

  // Update the CSS for all .riag-marker elements
  let style = document.getElementById('.maplibregl-popup-content');

  
  // if the style does not exist, append it
  if (!style) {
    style = document.createElement('style');
    style.id = '.maplibregl-popup-content';
    document.head.appendChild(style);
  }

  // otherwise, set visibility
  style.textContent = `
    .maplibregl-popup-content {
        width: 100%;
        height: 100%;
        padding: 1em;
        display: ${visible} !important;
        overflow: hidden;
        background-color: var(--background_color)
    }
  `;
}
