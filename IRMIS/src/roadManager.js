import { slugToPropertyGetter } from "./filter";
import { getRoadMetadata, getRoadsMetadata, getRoadsMetadataChunks, putRoadMetadata } from "./assets/assetsAPI";
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
document.addEventListener("estrada.road.filter.apply", (data) => {
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
            roadsLookup[roadMetadata.id] = roadMetadata;
            return roadsLookup;
        },
        roads,
    );
    dispatch("estrada.road.assetMetaDataAdded", { detail: { assets: roadList } });
}

export function saveRoad(sourceRoad) {
    return Promise.resolve(putRoadMetadata(sourceRoad))
        .then((road) => {
            roads[road.id] = road;
            dispatch("estrada.road.assetMetaDataUpdated", { detail: { asset: road } });
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
    const assetType = "ROAD";
    const idMap = filteredRoads.reduce((idMap, road) => {
        idMap[road.id] = true;
        return idMap;
    }, {});

    dispatch("estrada.road.filter.applied", { detail: { assetType, idMap } });
}
