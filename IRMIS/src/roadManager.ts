import { getRoadAuditData, getRoadMetadata, getRoadsMetadata, getRoadsMetadataChunks, putRoadMetadata } from "./assets/assets_api";

import { Road, Version } from "../protobuf/roads_pb";

const roads: { [name: string]: Road } = {};
let filteredRoads: { [name: string]: Road } = {};

// Get the road metadata chunk details
getRoadsMetadataChunks()
    .then((chunks) => {
        // for each chunk, download the roads
        chunks.forEach((chunk: any) => {
            getRoadsMetadata(chunk.road_type)
                .then((roadList) => {
                    // add the roads to the road manager
                    addRoadMetadata(roadList);
                });
        });
    });

// when a filter is applied filter the roads
document.addEventListener("estrada.filter.apply", (data) => {
    const filterState = (data as CustomEvent).detail.filterState;
    filterRoads(filterState);
});

export function getRoad(id: string | number) {
    const road = roads[id];
    if (road) {
        return Promise.resolve(road);
    }
    return getRoadMetadata(id);
}

function addRoadMetadata(roadList: any) {
    roadList.reduce(
        (roadsLookup: any, roadMetadata: any) => {
            roadsLookup[roadMetadata.getId()] = roadMetadata;
            return roadsLookup;
        },
        roads,
    );
    document.dispatchEvent(new CustomEvent("estrada.roadManager.roadMetaDataAdded", {detail: { roadList }}));
}

export function saveRoad(sourceRoad: Road): Promise<Road> {
    return Promise.resolve(putRoadMetadata(sourceRoad))
        .then((road: Road) => {
            roads[road.getId()] = road;
            document.dispatchEvent(new CustomEvent("estrada.table.roadMetaDataUpdated", {detail: {road}}));
            return road;
        });
}

export function getRoadAudit(roadId: string | number): Promise<Version[]> {
    return Promise.resolve(getRoadAuditData(roadId))
        .then((auditList) => {
            // document.dispatchEvent(new CustomEvent("estrada.auditTable.roadAuditDataAdded", {detail: {auditList}}));
            return auditList;
        });
}

function filterRoads(filterState: { [name: string]: any }) {
    const idMap: { [name: string]: boolean } = {};
    filteredRoads = {};

    Object.values(roads).forEach((road) => {
        // every filter state must match
        const includeRoad = Object.entries(filterState).every(([slug, values]) => {
            // empty array means all match
            if (values.length === 0) {
                return true;
            }
            // or some values of one state must match
            return values.some((value: any) => {
                const propertyGetter = slugToPropertyGetter[slug];
                return (road as any)[propertyGetter]() === value;
            });
        });

        if (includeRoad) {
            filteredRoads[road.getId().toString()] = road;
            idMap[road.getId().toString()] = true;
        }
    });

    // communicate the filter
    document.dispatchEvent(new CustomEvent("estrada.filter.applied", {detail: { idMap }}));
}

export function roadPopup(id: string | number) {
    const road = roads[id];
    const code = road.getRoadCode();
    const name = road.getRoadName();

    let html = "";

    if (code) {
        html += `
        <span class="popup">
            <span class="popup label">Code: </span>
            <span class="popup value">${code}</span>
        </span>`;
    }

    if (name) {
        html += `
        <span class="popup">
            <span class="popup label">Name: </span>
            <span class="popup value">${name}</span>
        </span>`;
    }

    return html;
}

// we'll need to add more in here as we add more filters
const slugToPropertyGetter: { [name: string]: string } = {
    road_code: "getRoadCode",
    road_type: "getRoadType",
    surface_type: "getSurfaceType",
    // tslint:disable-next-line: object-literal-sort-keys
    surface_condition: "getSurfaceCondition",
    road_status: "getRoadStatus",
    administrative_area: "getAdministrativeArea",
};
