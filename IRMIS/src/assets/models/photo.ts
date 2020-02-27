import { Photo } from "../../../protobuf/photo_pb";
import { IEstrada } from "./estradaBase";
import { getFieldName, getHelpText, makeEstradaObject } from "../protoBufUtilities";

// tslint:disable: max-classes-per-file

const photoSchema = {};

export class EstradaPhoto extends Photo implements IEstrada {
    public static getFieldName(field: string) {
        return getFieldName(photoSchema, field);
    }

    public static getHelpText(field: string) {
        return getHelpText(photoSchema, field);
    }

    get id() {
        return this.getId();
    }

    get description() {
        return this.getDescription() || "";
    }

    get url() {
        return this.getUrl() || "";
    }

    get fkLink() {
        return this.getFkLink() || "";
    }
}

export function makeEstradaPhoto(pbphoto: { [name: string]: any }): EstradaPhoto {
    return makeEstradaObject(EstradaPhoto, pbphoto) as EstradaPhoto;
}
