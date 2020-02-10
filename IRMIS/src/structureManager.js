import { getRoadStructuresMetadata, getStructureMetadata, getStructuresMetadata, postStructureData, putStructureData } from "./assets/structuresAPI";
import { dispatch } from "./assets/utilities";
import { slugToPropertyGetter } from "./filter";

export const structures = {};
let filteredStructures = {};

// Get all Structures metadata details
// add the list to the Structure Manager's master list
getStructuresMetadata()
    .then((sourceStructure) => {
        // Delete all keys from the existing structures object
        Object.keys(structures).forEach((key) => {
            delete structures[key];
        });

        // Add in all the ones that were returned
        const sourceObject = sourceStructure.getObject();
        Object.keys(sourceObject).forEach((key) => {
            structures[key] = sourceObject[key];
        });

        // Let everyone know
        const eventName = "estrada.structure.assetMetaDataAdded";
        const eventDetail = { detail: { assets: structures } };
        dispatch(eventName, eventDetail);
    });

// when a filter is applied filter the structures
document.addEventListener("estrada.structure.filter.apply", (data) => {
    const filterState = data.detail.filterState;
    filterStructures(filterState);
});

export function getStructure(id) {
    let structure = structures[id];
    if (structure) {
        return Promise.resolve(structure);
    }
    return getStructureMetadata(id);
}

export function getRoadStructures(roadId, structureType) {
    return getRoadStructuresMetadata(roadId, structureType);
}

export function createStructure(structure, structureType) {
    return Promise.resolve(postStructureData(structure, structureType))
        .then((structure) => {
            structures[structure.id] = structure;
            dispatch("estrada.structure.assetMetaDataCreated", { detail: { assets: structures } });
            return structure;
        });
}

export function updateStructure(structure, structureType) {
    return Promise.resolve(putStructureData(structure, structureType))
        .then((structure) => {
            structures[structure.id] = structure;
            dispatch("estrada.structure.assetMetaDataUpdated", { detail: { asset: structure } });
            return structure;
        });
}

export function getStructureAudit(structureId) {
    return Promise.resolve(getStructureAuditData(structureId))
        .then((auditList) => {
            // dispatch("estrada.auditTable.structureAuditDataAdded", { detail: { auditList } });
            return auditList;
        });
}

function filterStructures(filterState) {
    filteredStructures = Object.values(structures).filter( structure => {
        // every filter state must match
        return Object.entries(filterState).every(([slug, values]) => {
            // empty array means all match
            if (!values.length) {
                return true;
            }

            // or some values of one state must match
            return values.some(value => {
                const propertyGetter = slugToPropertyGetter[slug];
                const propertyGetterType = typeof structure[propertyGetter];
                switch (propertyGetterType) {
                    case "function":
                        return structure[propertyGetter]() === value;
                    case "undefined":
                        // This indicates a programming error,
                        // but we're returning everything in this case
                        return true;
                    default:
                        return structure[propertyGetter] === value;
                }
            });
        });
    });

    // communicate the filter
    const assetType = "STRC";
    const idMap = filteredStructures.reduce((idMap, structure) => {
        idMap[structure.id] = true;
        return idMap;
    }, {});

    dispatch("estrada.structure.filter.applied", { detail: { assetType, idMap } });
}
