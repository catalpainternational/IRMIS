import { getRoadMetadata, getRoadsMetadata, getRoadsMetadataChunks, putRoadMetadata } from "./assets/assetsAPI";
import { dispatch } from "./assets/utilities";
import { filterAssets } from "./assets/filterUtilities";

import $ from "jquery";

export const roads = {};
let filteredRoads = {};

// Get the road metadata chunk details
export function getMetadataChunksForRoads() {
    getRoadsMetadataChunks()
        .then((chunks) => {
            $("#assets-loading").modal("show");
            const big_chunks = {};
            chunks.forEach((chunk) => {
                big_chunks[chunk.asset_class] = big_chunks[chunk.asset_class] || {
                    asset_class: chunk.asset_class,
                    asset_code_prefix: "",
                    id__count: 0
                };

                big_chunks[chunk.asset_class].id__count += chunk.id__count;
            });
            let prepared_chunks = [];
            Object.keys(big_chunks).forEach((asset_class) => {
                if (big_chunks[asset_class].id__count < 1000) {
                    prepared_chunks.push(big_chunks[asset_class]);
                } else {
                    const asset_class_chunks = chunks.filter((chunk) => chunk.asset_class === asset_class);
                    prepared_chunks = prepared_chunks.concat(asset_class_chunks);
                }
            });
            // for each chunk, download the roads
            let estradaRoads = [];
            prepared_chunks.forEach((chunk) => {
                estradaRoads.push(getRoadsMetadata(`${chunk.asset_class}_${chunk.asset_code_prefix}`));
            });
            Promise.all(estradaRoads).then((values) => {
                const flattenValues = [].concat(...values);
                addRoadMetadata(flattenValues);
                $("#assets-loading").modal("hide");
            });
        });
}

// when a filter is applied filter the roads
document.addEventListener("estrada.road.filter.apply", (data) => {
    const filterState = data.detail.filter;
    filteredRoads = filterAssets(filterState, roads, "estrada.road.filter.applied");
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
