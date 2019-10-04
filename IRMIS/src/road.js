import proj4 from "proj4";

import { Road, Roads } from "../protobuf/roads_pb";

var roadSchema = JSON.parse(document.getElementById('road_schema').textContent);

function humanizeChoices(choiceField, valueKey=false, displayKey=false) {
    let values = {};
    valueKey = valueKey || 0;
    displayKey = displayKey || 1;
    roadSchema[choiceField].options.forEach(function(o){
        values[o[valueKey]] = o[displayKey];
    });
    return values;
}

// utility function to pick from choices if value is truthy, or return empty string
function choice_or_empty(value, choices) {
    return value ? choices[value] : '';
}

const ROAD_STATUS_CHOICES = humanizeChoices('road_status', 'code', 'name');
const ROAD_TYPE_CHOICES = humanizeChoices('road_type');
const SURFACE_TYPE_CHOICES = humanizeChoices('surface_type', 'code', 'name');
const SURFACE_CONDITION_CHOICES = humanizeChoices('surface_condition');
const PAVEMENT_CLASS_CHOICES = humanizeChoices('pavement_class', 'code', 'name');
const ADMINISTRATIVE_AREA_CHOICES = humanizeChoices('administrative_area', 'id', 'name');
const TECHNICAL_CLASS_CHOICES = humanizeChoices('technical_class', 'code', 'name');
const MAINTENANCE_NEED_CHOICES = humanizeChoices('maintenance_need', 'code', 'name');
const TRAFFIC_LEVEL_CHOICES = humanizeChoices('traffic_level');

function toChainageFormat(value) {
    const distance = parseFloat(value).toFixed(0);
    const meters = `000${distance.substr(-3)}`.substr(-3);
    const kilometers = `${distance.substr(0, distance.length - 3)}` || 0;

    return `${kilometers}+${meters}`;
}

// INPUT FORMAT: EPSG:32751 WGS 84 / UTM zone 51S - OUTPUT FORMAT: EPSG:4326 WGS 84
proj4.defs("EPSG:32751", "+proj=utm +zone=51 +south +ellps=WGS84 +datum=WGS84 +units=m +no_defs");
const projToWGS84 = proj4("EPSG:32751", "WGS84");

const modf = (number) => {
    // JS implementation of Python math -> modf() function
    // split a number into interger and remainder values
    // returned items have same sign as original number
    return [number % 1, Math.trunc(number)];
}

const splitOutDms = (coord) => {
    const split_deg = modf(coord);
    const degrees = Math.trunc(split_deg[1]);
    const interm = modf(split_deg[0] * 60);
    const minutes = Math.abs(Math.trunc(interm[1]));
    const seconds = Math.abs(Math.round((interm[0] * 60 + 0.00001) * 100) / 100);
    
    return [degrees, minutes, seconds];
}

const toDms = (lat_long) => {
    if (!lat_long) {
        return "";
    }

    const x_dms = splitOutDms(lat_long[0]);
    const y_dms = splitOutDms(lat_long[1]);

    // calculate N/S (lat) & E/W (long)
    const NorS = (y_dms[0] < 0) ? "S" : "N";
    const EorW = (x_dms[0] < 0) ? "W" : "E";

    // return formatted DMS string
    return `${Math.abs(y_dms[0])}\u00b0${y_dms[1]}'${y_dms[2]}"${NorS} ${Math.abs(x_dms[0])}\u00b0${x_dms[1]}'${x_dms[2]}"${EorW}`;
}

const toUtm = (lat_long) => {
    return lat_long
        ? `${lat_long[0].toFixed(5)}, ${lat_long[1].toFixed(5)}`
        : "";
}

export class EstradaRoad extends Road {

    get id() {
        return this.getId();
    }

    get name() {
        return this.getRoadName();
    }

    get code() {
        return this.getRoadCode();
    }

    get linkName() {
        return `${this.getLinkStartName()} - ${this.getLinkEndName()}`;
    }

    get linkStartName() {
        return this.getLinkStartName();
    }

    get linkStartChainage() {
        return toChainageFormat(this.getLinkStartChainage());
    }

    get linkEndName() {
        return this.getLinkEndName();
    }

    get linkEndChainage() {
        return toChainageFormat(this.getLinkEndChainage());
    }

    get linkCode() {
        return this.getLinkCode();
    }

    get linkLength() {
        return parseFloat(this.getLinkLength()).toFixed(2);
    }

    get status() {
        return choice_or_empty(this.getRoadStatus(), ROAD_STATUS_CHOICES);
    }

    get type() {
        return choice_or_empty(this.getRoadType(), ROAD_TYPE_CHOICES);
    }

    get surfaceType() {
        return choice_or_empty(this.getSurfaceType(), SURFACE_TYPE_CHOICES);
    }

    get surfaceCondition() {
        return choice_or_empty(this.getSurfaceCondition(), SURFACE_CONDITION_CHOICES);
    }

    get pavementClass() {
        return choice_or_empty(this.getPavementClass(), PAVEMENT_CLASS_CHOICES);
    }

    get administrativeArea() {
        return choice_or_empty(parseInt(this.getAdministrativeArea()), ADMINISTRATIVE_AREA_CHOICES);
    }

    get carriagewayWidth() {
        return parseFloat(this.getCarriagewayWidth()).toFixed(1);
    }

    get project() {
        return this.getProject();
    }

    get fundingSource() {
        return this.getFundingSource();
    }

    get technicalClass() {
        return choice_or_empty(this.getTechnicalClass(), TECHNICAL_CLASS_CHOICES);
    }

    get maintenanceNeed() {
        return choice_or_empty(this.getMaintenanceNeed(), MAINTENANCE_NEED_CHOICES);
    }

    get trafficLevel() {
        return choice_or_empty(this.getTrafficLevel(), TRAFFIC_LEVEL_CHOICES);
    }

    get projectionStart() {
        return this.getProjectionStart();
    }

    get projectionEnd() {
        return this.getProjectionEnd();
    }

    get startDMS() {
        return toDms(projToWGS84.forward(this.getProjectionStart().array));
    }

    get endDMS() {
        return toDms(projToWGS84.forward(this.getProjectionEnd().array));
    }

    get startUTM() {
        return toUtm(projToWGS84.forward(this.getProjectionStart().array));
    }

    get endUTM() {
        return toUtm(projToWGS84.forward(this.getProjectionEnd().array));
    }

}

export function getFieldName(field) {
    if (roadSchema[field]) { return roadSchema[field].display; }
    else { return ""; }
}

export function getHelpText(field) {
    if (roadSchema[field]) { return roadSchema[field].help_text; }
    else { return ""; }
}
