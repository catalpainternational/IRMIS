import { getRoadMetadata, getRoadsMetadata, getRoadsMetadataChunks, putRoadMetadata } from "./assets/assets_api";
import { slugToPropertyGetter } from "./filter";

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
        .then(road => {
            roads[road.getId()] = road;
            document.dispatchEvent(new CustomEvent("estrada.table.roadMetaDataUpdated", {detail: {road}}));
            return road;
        });
}

function filterRoads(filterState) {
    filteredRoads = Object.values(roads).filter( road => {
        // every filter state must match
        return Object.entries(filterState).every(([slug, values]) => {
            // empty array means all match
            if (!values.length) {
                return true;
            }
            
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

/** Get a subset of information (code and name) for use in building a popup on the map */
export function getRoadPopupData(id) {
    const road = roads[id];
    const roadPopupData = {};
    if (!road) {
        // If the user clicks on the road in the map before the data is in protoBuf
        // we may not have the matching info to show them.
        // So just exit politely.
        roadPopupData[window.gettext("Data")] = window.gettext("Loading");
        return roadPopupData;
    }

    let code, name;
    if (code = road.getRoadCode()) {
        roadPopupData.Code = code;
    }
    if (name = road.getRoadName()) {
        roadPopupData.Name = name;
    };
    
    return roadPopupData;
}
