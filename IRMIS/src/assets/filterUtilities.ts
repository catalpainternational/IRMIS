import { slugToPropertyGetter } from "../filterSlugs";
import { Filter } from "./models/filter";
import { dispatch } from "./utilities";

export function filterAssets(
    filter: Filter,
    assets: { [name: string]: any },
    eventName: string,
): any[] {
    const filteredAssets = Object.values(assets).filter((asset) => {
        // every filter state must match
        return filter.filters().every(([slug, values]) => {
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
    const idMap: { [name: string]: boolean } = {};
    filteredAssets.forEach((asset) => { idMap[asset.id] = true; });

    dispatch(eventName, { detail: { assetType: filter.assetType, idMap } });

    return filteredAssets;
}
