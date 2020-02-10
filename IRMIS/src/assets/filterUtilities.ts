import { slugToPropertyGetter } from "../filterSlugs";
import { dispatch } from "./utilities";

export function filterAssets(
    filterState: { [name: string]: any },
    assets: { [name: string]: any },
    eventName: string,
    assetType: string,
): any[] {
    const filteredStructures = Object.values(assets).filter((asset) => {
        // every filter state must match
        return Object.entries(filterState).every(([slug, values]) => {
            // empty array means all match
            if (!values.length) {
                return true;
            }

            // or some values of one state must match
            return values.some((value: any) => {
                const propertyGetter = slugToPropertyGetter[slug];
                const propertyGetterType = typeof asset[propertyGetter];
                switch (propertyGetterType) {
                    case "function":
                        return asset[propertyGetter]() === value;
                    case "undefined":
                        // This indicates a programming error,
                        // but we're returning everything in this case
                        return true;
                    default:
                        return asset[propertyGetter] === value;
                }
            });
        });
    });

    // communicate the filter
    const idMap = filteredStructures.reduce((idMap, structure) => {
        idMap[structure.id] = true;
        return idMap;
    }, {});

    dispatch(eventName, { detail: { assetType, idMap } });

    return filteredStructures;
}
