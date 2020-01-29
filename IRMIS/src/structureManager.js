import { getRoadStructuresMetadata, getStructureMetadata, getStructuresMetadata, postStructureData, putStructureData } from "./assets/structuresAPI";
import { dispatch } from "./assets/utilities";
import { slugToPropertyGetter } from "./filter";

export const structures = {};
let filteredStructures = {};

// Get the structure metadata details
// for each Structure type download the Structures
["bridge", "culvert"].forEach((t) => {
    getStructuresMetadata(t)
        .then((structureList) => {
            // add the structures to the structure manager
            addStructureMetadata(structureList);
        });
});

// when a filter is applied filter the structures
document.addEventListener("estrada.filter.apply", (data) => {
    const filterState = data.detail.filterState;
    filterStructures(filterState);
});

function addStructureMetadata(structureList) {
    structureList.reduce(
        (structuresLookup, structureMetadata) => {
            structuresLookup[structureMetadata.getId()] = structureMetadata;
            return structuresLookup;
        },
        structures,
    );
    dispatch("estrada.structureManager.structureMetaDataAdded", { detail: { structureList } });
}

export function getStructure(id, structureType) {
    let structure = structures[id];
    if (structure) {
        return Promise.resolve(structure);
    }

    return getStructureMetadata(id, structureType);
}

export function getRoadStructures(roadId, structureType) {
    return getRoadStructuresMetadata(roadId, structureType);
}

export function createStructure(structure, structureType) {
    return Promise.resolve(postStructureData(structure, structureType))
        .then((structure) => {
            structures[structure.getId()] = structure;
            dispatch("estrada.table.structureMetaDataCreated", { detail: { structure } });
            return structure;
        });
}

export function updateStructure(structure, structureType) {
    return Promise.resolve(putStructureData(structure, structureType))
        .then((structure) => {
            structures[structure.getId()] = structure;
            dispatch("estrada.table.structureMetaDataUpdated", { detail: { structure } });
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
                let propertyGetter = slugToPropertyGetter[slug];
                return structure[propertyGetter]() === value;
            });
        });
    });

    // communicate the filter
    let idMap = filteredStructures.reduce((idMap, structure) => {
        idMap[structure.getId().toString()] = true;
        return idMap;
    }, {});

    dispatch("estrada.filter.applied", { detail: { idMap } });
}
