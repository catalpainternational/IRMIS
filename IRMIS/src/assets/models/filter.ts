import { dispatch } from "../utilities";

export class Filter {
    private filterAssetType: string = "ROAD";
    private filterState: { [name: string]: any[] } = {};

    /** Returns a restricted assetType, either "ROAD" or "STRC" */
    get assetType() {
        return ["STRC", "BRDG", "CULV"].includes(this.filterAssetType)
            ? "STRC" : "ROAD";
    }

    constructor(assetType: string) {
        this.filterAssetType = assetType;
    }

    /** applies or unapplies the value to the slug filter */
    public toggle(slug: string, value: any) {
        this.initialise(slug);
        const slugFilterValues = this.filterState[slug];
        const index = slugFilterValues.indexOf(value);
        if (index === -1) {
            slugFilterValues.push(value);
        } else {
            slugFilterValues.splice(index, 1);
        }
        this.apply();
    }

    /** ensures the slug filterstate is ready for adding values */
    public initialise(slug: string) {
        this.filterState[slug] = this.filterState[slug] || [];
    }

    /** is slug=value filter active */
    public isFilterApplied(slug: string, value: any) {
        this.initialise(slug);
        return this.filterState[slug].indexOf(value) !== -1;
    }

    public filters() {
        return Object.entries(this.filterState);
    }

    /** clear a slug filter */
    public clear(slug: string) {
        this.filterState[slug].length = 0;
        this.apply();
    }

    /** clear all slug filters */
    public clearAll() {
        this.filterState = {};
        this.apply();
    }

    /** actually make the filter happen */
    public apply() {
        const eventName = this.assetType === "ROAD"
            ? "estrada.road.filter.apply"
            : "estrada.structure.filter.apply";
        dispatch(eventName, { detail: { filter: this } });
    }
}
