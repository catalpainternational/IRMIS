import { filterRows } from "./table.js";
import { filterFeatures } from "./map/utilities/filterGeoJSON";

export class RoadManager {
    
    constructor() {
        this.roads = {}
        this.filteredRoads = {}
    }

    add(roadList) {
        roadList.reduce(
            (roadsLookup, roadMetadata) => {
                roadsLookup[roadMetadata.getId()] = roadMetadata;
                return roadsLookup;
            },
            this.roads,
        );
    }

    getRoads() {
        return Object.values(this.roads);
    }

    getRoad(id) {
        return this.roads[id];
    }

    filterRoads(filterState) {
        this.filteredRoads = Object.values(this.roads).filter( road => {
            // every filter state must match
            return Object.entries(filterState).every(([slug, values]) => {
                // empty array means all match
                if (values.length === 0) return true;
                // or some values of one state must match
                return values.some(value => {
                    let propertyGetter = slugToPropertyGetter[slug];
                    return road[propertyGetter]() === value;
                });
            });
        });

        // communicate the filter
        let idMap = {};

        this.filteredRoads.forEach(r => idMap[r.getId().toString()] = true);
        filterRows(idMap);
        filterFeatures(idMap);
    }

    roadPopup(id) {
        const road = this.getRoad(id);
        var code, name;
        let html = '';
        if (code = road.getRoadCode()) {
            html += `
            <span class="popup">
                <span class="popup label">Code: </span>
                <span class="popup value">${code}</span>
            </span>`;
        }
        if (name = road.getRoadName()) {
            html += `
            <span class="popup">
                <span class="popup label">Name: </span>
                <span class="popup value">${name}</span>
            </span>`;
        }
        return html;
    }
}

// we'll need to add more in here as we add more filters
const slugToPropertyGetter = {
    road_code: 'getRoadCode',
    road_type: 'getRoadType',
    surface_type: 'getSurfaceType',
    surface_condition: 'getSurfaceCondition',
    road_status: 'getRoadStatus',
    administrative_area: 'getAdministrativeArea',
};
