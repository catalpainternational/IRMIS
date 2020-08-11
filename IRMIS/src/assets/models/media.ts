import dayjs from "dayjs";

import { Media } from "../../../protobuf/media_pb";
import { IEstrada } from "./estradaBase";
import { getFieldName, getHelpText, makeEstradaObject } from "../protoBufUtilities";

// Do a reexport for the benefit of anything that references EstradaMedia
export { Media, Medias } from "../../../protobuf/media_pb";

// tslint:disable: max-classes-per-file

const mediaSchema = {};

export class EstradaMedia extends Media implements IEstrada {
    public static getFieldName(field: string) {
        return getFieldName(mediaSchema, field);
    }

    public static getHelpText(field: string) {
        return getHelpText(mediaSchema, field);
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

    get user() {
        return this.getUser() || "";
    }

    get addedBy() {
        return this.getAddedBy() || "";
    }

    get dateCreated() {
        // Note getDateCreated doesn't actually return a proper Timestamp object
        const pbufData = this.getDateCreated() as ({ [name: string]: any } | undefined);
        if (!pbufData || !pbufData.array || !pbufData.array.length) {
            return "";
        }
        const date = dayjs(new Date(pbufData.array[0] * 1000));
        return date.isValid() ? date.format("YYYY-MM-DD") : "";
    }
}

export function makeEstradaMedia(pbmedia: { [name: string]: any }): EstradaMedia {
    return makeEstradaObject(EstradaMedia, pbmedia) as EstradaMedia;
}
