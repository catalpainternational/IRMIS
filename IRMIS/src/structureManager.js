import { slugToPropertyGetter } from "./filter";
import { getStructureAuditData, getStructureMetadata, getStructuresMetadata, getStructuresMetadataChunks, putStructureMetadata } from "./assets/assets_api";
import { dispatch } from "./assets/utilities";

export const structures = {};
let filteredStructures = {};

// Get the structure metadata chunk details
getStructuresMetadataChunks()
    .then((chunks) => {
        // for each chunk, download the structures
        chunks.forEach((chunk) => {
            getStructuresMetadata(chunk.structure_type)
                .then((structureList) => {
                    // add the structures to the structure manager
                    addStructureMetadata(structureList);
                });
        });
    });

// when a filter is applied filter the structures
document.addEventListener("estrada.filter.apply", (data) => {
    const filterState = data.detail.filterState;
    filterStructures(filterState);
});

export function getStructure(id) {
    const structure = structures[id];
    if (structure) {
        return Promise.resolve(structure);
    }
    return getStructureMetadata(id);
}

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

export function saveStructure(sourceStructure) {
    return Promise.resolve(putStructureMetadata(sourceStructure))
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
