import { getRoadMetadata, getRoadsMetadata, getRoadsMetadataChunks, putRoadMetadata } from "./assets/assets_api";

let roads = {}
let filteredRoads = {}

// Get the road metadata chunk details
getRoadsMetadataChunks()
    .then(chunks => {
        // for each chunk, download the roads
        chunks.forEach(chunk => {
            getRoadsMetadata(chunk.road_type)
                .then(roadList => {
                    // add the roads to the road manager
                    addRoadMetadata(roadList);
                });
        });
    });

// when a filter is applied filter the roads
document.addEventListener('estrada.filter.apply', (data) => {
    const filterState = data.detail.filterState;
    filterRoads(filterState);
});

export function getRoad(id) {
    let road = roads[id];
    if(road) return Promise.resolve(road);
    return getRoadMetadata(id);
}

function addRoadMetadata(roadList) {
    roadList.reduce(
        (roadsLookup, roadMetadata) => {
            roadsLookup[roadMetadata.getId()] = roadMetadata;
            return roadsLookup;
        },
        roads,
    );
    document.dispatchEvent(new CustomEvent("estrada.roadManager.roadMetaDataAdded", {"detail": { roadList }}));
}

export function saveRoad(road) {
    return Promise.resolve(putRoadMetadata(road))
        .then((response) => {
            let result;
            debugger;
            switch (response.status) {
                case 204:
                    result = true;
                    break;
                case 400:
                case 409:
                    result = false;
                    break;
                default:
                    result = false;
                    break;
            };
             return result;
        });
}

function filterRoads(filterState) {
    filteredRoads = Object.values(roads).filter( road => {
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
    let idMap = filteredRoads.reduce((idMap, road) => {
        idMap[road.getId().toString()] = true;
        return idMap;
    }, {});
    document.dispatchEvent(new CustomEvent("estrada.filter.applied", {"detail": { idMap }}));
}

export function roadPopup(id) {
    const road = roads[id];
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

// we'll need to add more in here as we add more filters
const slugToPropertyGetter = {
    road_code: 'getRoadCode',
    road_type: 'getRoadType',
    surface_type: 'getSurfaceType',
    surface_condition: 'getSurfaceCondition',
    road_status: 'getRoadStatus',
    administrative_area: 'getAdministrativeArea',
};
