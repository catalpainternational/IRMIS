import dayjs from "dayjs";

import { Plan, Snapshot } from "../../../protobuf/plan_pb";
import { IEstrada } from "./estradaBase";

import { choice_or_default, getFieldName, getHelpText, makeEstradaObject } from "../protoBufUtilities";
import { ASSET_CLASS_CHOICES } from "./choices";

// We may need a plan schema - primarily for formatted field names
// JSON.parse(document.getElementById('plan_schema').textContent);
const planSchema = {};
const snapshotSchema = {};

// tslint:disable: max-classes-per-file

export class EstradaPlan extends Plan implements IEstrada {
    public static getFieldName(field: string) {
        return getFieldName(planSchema, field);
    }

    public static getHelpText(field: string) {
        return getHelpText(planSchema, field);
    }

    get id() {
        return this.getId();
    }

    get title() {
        return this.getTitle();
    }

    set title(value: string) {
        this.setTitle(value);
    }

    get url() {
        return this.getUrl();
    }

    set url(value: any) {
        this.setUrl(value);
    }

    get fileName() {
        return this.getFileName();
    }

    set file(value: BinaryType) {
        this.setFile(value);
    }

    get user() {
        return this.getUser() || "";
    }

    get addedBy() {
        return this.getAddedBy() || "";
    }

    get dateCreated() {
        const pbufData = this.getDateCreated() as ({ [name: string]: any } | undefined);
        if (!pbufData || !pbufData.array || !pbufData.array.length) {
            return "";
        }
        const date = dayjs(new Date(pbufData.array[0] * 1000));
        return date.isValid() ? date.format("YYYY-MM-DD HH:mm") : "";
    }

    get lastModified() {
        const pbufData = this.getLastModified() as ({ [name: string]: any } | undefined);
        if (!pbufData || !pbufData.array || !pbufData.array.length) {
            return "";
        }
        const date = dayjs(new Date(pbufData.array[0] * 1000));
        return date.isValid() ? date.format("YYYY-MM-DD HH:mm") : "";
    }

    get approved() {
        return this.getApproved() || false;
    }

    set approved(value: boolean) {
        this.setApproved(value);
    }

    get assetClass() {
        return choice_or_default(this.getAssetClass(), ASSET_CLASS_CHOICES);
    }

    get summary() {
        return this.getSummaryList() || [];
    }
}

export class EstradaSnapshot extends Snapshot implements IEstrada {
    public static getFieldName(field: string) {
        return getFieldName(snapshotSchema, field);
    }

    public static getHelpText(field: string) {
        return getHelpText(snapshotSchema, field);
    }

    get id() {
        return this.getId();
    }

    get year() {
        return this.getYear();
    }

    get budget() {
        return this.getBudget();
    }

    get length() {
        return this.getLength();
    }

    get assetClass() {
        return this.getAssetClass();
    }

    get workType() {
        return this.getWorkType();
    }
}

export function makeEstradaPlan(pbplan: { [name: string]: any }): EstradaPlan {
    return makeEstradaObject(EstradaPlan, pbplan) as EstradaPlan;
}

export function makeEstradaSnapshot(pbsnapshot: { [name: string]: any }): EstradaSnapshot {
    return makeEstradaObject(EstradaSnapshot, pbsnapshot) as EstradaSnapshot;
}
