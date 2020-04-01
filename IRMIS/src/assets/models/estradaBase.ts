export interface IEstrada {
    id: string | number;
    getId(): string | number;
}

export interface IAsset extends IEstrada {
    // Asset Ids can only be strings
    id: string;
    name: string;
    code: string;

    /** The asset's type - the prefix part of its Id */
    assetType: string;
    /** The asset's type name - in the currently selected language */
    assetTypeName: string;
    /** The asset's Id without the assetType prefix */
    assetId: string;

    // public static methods
    getFieldName(field: string): string;
    // getHelpText(field: string): string;
}
