
const mapState = {
    activeTooltipTimeout: null,
    isIframeTransitionActive: false,
    pendingWikiUri: '',
    currentHoveredFeatureId: null
};


export function add_poi_tooltip(map, layername = '', popup) {
    if (!map || !layername || !popup) return;

    map.on('mouseenter', layername, (e) => {
        // 1. Sofortige UI-Reaktion und Abbruch des Schliess-Timers
        map.getCanvas().style.cursor = 'pointer';
        if (mapState.activeTooltipTimeout) {
            clearTimeout(mapState.activeTooltipTimeout);
            mapState.activeTooltipTimeout = null;
        }

        const radius = 15; // 10-15px ist Industrie-Standard für Touch/Maus-Toleranz (100px ist oft zu gross)
        const bbox = [
            [e.point.x - radius, e.point.y - radius],
            [e.point.x + radius, e.point.y + radius]
        ];

        const features = map.queryRenderedFeatures(bbox, { layers: [layername] });
        const feature = features[0] || e.features[0];
        if (!feature || !feature.properties) return;

        const featureId = feature.id || feature.properties.name;
        if (mapState.currentHoveredFeatureId === featureId && popup.isOpen()) return;
        mapState.currentHoveredFeatureId = featureId;

        const name = feature.properties.name || 'Unbekannter Ort';
        let coordinates = feature.geometry.coordinates.slice();
        const targetCenter = [coordinates[0], coordinates[1] + 0.0002];

        while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
            coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
        }

        const offsetCoordinates = targetCenter;

        popup.setLngLat(offsetCoordinates)
             .setHTML(`<div class="poi-tooltip-content">${name}</div>`)
             .addTo(map);
    });
}


export function add_poi_iframe(map, layername = '', popup) {
    if (!map || !layername || !popup) return;

    map.on('click', layername, (e) => {
        const feature = e.features[0];
        if (!feature || !feature.properties?.wiki_article) return;

        if (mapState.activeTooltipTimeout) {
            clearTimeout(mapState.activeTooltipTimeout);
        }

        map.getCanvas().style.cursor = 'pointer';
        
        mapState.pendingWikiUri = feature.properties.wiki_article;
        mapState.isIframeTransitionActive = true;

        const coordinates = feature.geometry.coordinates.slice();
        const targetCenter = [coordinates[0] - 0.001, coordinates[1]];

        map.flyTo({
            center: targetCenter,
            zoom: 16,
            speed: 1.2,
            essential: true
        });
    });

    map.on('moveend', () => {
        if (!mapState.isIframeTransitionActive || !mapState.pendingWikiUri) return;

        const iframeSource = encodeURI(mapState.pendingWikiUri);
        const wikipediaIframe = `<iframe class="container" id="wiki_iframe" src="${iframeSource}" style="border:none; width:100%; height:100%;"></iframe>`;
        
        const bounds = map.getBounds();
        const topLeftCoordinates = [bounds.getWest(), bounds.getNorth()];
        
        popup.setHTML(wikipediaIframe)
             .setLngLat(topLeftCoordinates)
             .addTo(map);

        mapState.isIframeTransitionActive = false;
        mapState.pendingWikiUri = '';
        mapState.currentHoveredFeatureId = null;
    });
}


export function remove_poi_tooltip(map, layername = '', popup) {
    if (!map || !layername || !popup) return;

    map.on('mouseleave', layername, () => {
        map.getCanvas().style.cursor = '';
        mapState.currentHoveredFeatureId = null;

        if (mapState.activeTooltipTimeout) {
            clearTimeout(mapState.activeTooltipTimeout);
        }

        mapState.activeTooltipTimeout = setTimeout(() => {
            if (popup.isOpen() && !mapState.isIframeTransitionActive) {
                popup.remove();
            }
        }, 150);
    });
}