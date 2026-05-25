export async function loadIcons(map){

    const bus = await map.loadImage('./mapstyles/icons/custom_bus.png');
    const no_parking = await map.loadImage('./mapstyles/icons/custom_no_parking.png');
    const parking = await map.loadImage('./mapstyles/icons/custom_parking.png');
    const hotel_bed = await map.loadImage('./mapstyles/icons/custom_hotel_bed.png');
    const restaurant = await map.loadImage('./mapstyles/icons/custom_restaurant.png');
    const castle = await map.loadImage('./mapstyles/icons/custom_castle.png');
    const ship = await map.loadImage('./mapstyles/icons/custom_ship.png');
    const start = await map.loadImage('./mapstyles/icons/custom_start.png');

    map.addImage('custom_bus', bus.data);
    map.addImage('custom_no_parking', no_parking.data);
    map.addImage('custom_parking', parking.data);
    map.addImage('custom_hotel', hotel_bed.data);
    map.addImage('custom_restaurant', restaurant.data);
    map.addImage('custom_castle', castle.data);
    map.addImage('custom_ship', ship.data);
    map.addImage('custom_start', start.data);
}