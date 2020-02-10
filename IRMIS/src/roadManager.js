import { getRoadMetadata, getRoadsMetadata, getRoadsMetadataChunks, putRoadMetadata } from "./assets/assetsAPI";
import { dispatch } from "./assets/utilities";
import { filterAssets } from "./assets/filterUtilities";

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
    filteredRoads = filterAssets(filterState, roads, "estrada.road.filter.applied", "ROAD");
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
