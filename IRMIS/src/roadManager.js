import { slugToPropertyGetter } from "./filter";
import { getRoadAuditData, getRoadMetadata, getRoadsMetadata, getRoadsMetadataChunks, putRoadMetadata } from "./assets/assets_api";

const roads = {};
let filteredRoads = {};

// Get the road metadata chunk details
getRoadsMetadataChunks()
    .then((chunks) => {
        // for each chunk, download the roads
        chunks.forEach((chunk) => {
            getRoadsMetadata(chunk.road_type)
                .then((roadList) => {
                    // add the roads to the road manager
                    addRoadMetadata(roadList);
                });
        });
    });

// when a filter is applied filter the roads
document.addEventListener("estrada.filter.apply", (data) => {
    const filterState = data.detail.filterState;
    filterRoads(filterState);
});

export function getRoad(id) {
    const road = roads[id];
    if (road) {
        return Promise.resolve(road);
    }
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
    document.dispatchEvent(new CustomEvent("estrada.roadManager.roadMetaDataAdded", {detail: { roadList }}));
}

export function saveRoad(sourceRoad) {
    return Promise.resolve(putRoadMetadata(sourceRoad))
        .then((road) => {
            roads[road.getId()] = road;
            document.dispatchEvent(new CustomEvent("estrada.table.roadMetaDataUpdated", {detail: {road}}));
            return road;
        });
}

export function getRoadAudit(roadId) {
    return Promise.resolve(getRoadAuditData(roadId))
        .then((auditList) => {
            // document.dispatchEvent(new CustomEvent("estrada.auditTable.roadAuditDataAdded", {detail: {auditList}}));
            return auditList;
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

export function roadPopup(id) {
    const road = roads[id];
    if (!road) {
        // If the user clicks on the road in the map before the data is in protoBuf
        return `<span class="popup"><span class="popup label">${window.gettext("Loading")}</span></span>`;
    }
    const code = road.getRoadCode();
    const name = road.getRoadName();

    let html = "";

    if (code) {
        html += `<span class="popup"><span class="popup label">${window.gettext("Code")}: </span><span class="popup value">${code}</span></span>`;
    }

    if (name) {
        html += `<span class="popup"><span class="popup label">${window.gettext("Name")}: </span><span class="popup value">${name}</span> </span>`;
    }

    return html;
}
