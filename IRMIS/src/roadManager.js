import { slugToPropertyGetter } from "./filter";
import { getRoadAuditData, getRoadMetadata, getRoadsMetadata, getRoadsMetadataChunks, putRoadMetadata } from "./assets/assetsAPI";
import { dispatch } from "./assets/utilities";

export const roads = {};
let filteredRoads = {};

// Get the road metadata chunk details
getRoadsMetadataChunks()
    .then((chunks) => {
        // for each chunk, download the roads
        chunks.forEach((chunk) => {
            getRoadsMetadata(chunk.road_type) // Actually asset_class
                .then((roadList) => {
                    // add the roads to the road manager
                    addRoadMetadata(roadList);
                });
        });
    });

// when a filter is applied filter the roads
document.addEventListener("estrada.roadTable.filter.apply", (data) => {
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
    dispatch("estrada.roadManager.roadMetaDataAdded", { detail: { roadList } });
}

export function saveRoad(sourceRoad) {
    return Promise.resolve(putRoadMetadata(sourceRoad))
        .then((road) => {
            roads[road.getId()] = road;
            dispatch("estrada.roadTable.roadMetaDataUpdated", { detail: { road } });
            return road;
        });
}

export function getRoadAudit(roadId) {
    return Promise.resolve(getRoadAuditData(roadId))
        .then((auditList) => {
            // dispatch("estrada.auditTable.roadAuditDataAdded", { detail: { auditList } });
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

    dispatch("estrada.roadTable.filter.applied", { detail: { idMap } });
}
