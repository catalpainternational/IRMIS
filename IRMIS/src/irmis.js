import './styles/irmis.scss';
var road_api = require('./js/roads_api.js');

console.log("Getting list of Roads MetaData...");
road_api.getRoadMetadata();

console.log("Getting single Road GeoData...");
road_api.getRoadGeometry(903);
