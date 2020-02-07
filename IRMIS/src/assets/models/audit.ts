import { Version } from "../../../protobuf/version_pb";

import { getFieldName, getHelpText, makeEstradaObject } from "../protoBufUtilities";
import { IEstrada } from "./estradaBase";

const auditSchema = {
    comment: { display: (window as any).gettext("Description") },
    dateCreated: { display: (window as any).gettext("Date") },
    id: { display: "Id" },
    user: { display: (window as any).gettext("User") },
};

export class EstradaAudit extends Version implements IEstrada {
    public static getFieldName(field: string) {
        return getFieldName(auditSchema, field);
    }

    public static getHelpText(field: string) {
        return getHelpText(auditSchema, field);
    }

    public getId() {
        return this.getPk();
    }

    get id() {
        return this.getPk();
    }

    get dateCreated() {
        return this.hasDateCreated()
            ? new Date(this.getDateCreated()!.getSeconds() * 1000)
            : undefined;
    }

    get user() {
        return this.getUser();
    }

    get comment() {
        return this.getComment();
    }
}

export function makeEstradaAudit(pbversion: { [name: string]: any }): EstradaAudit {
    return makeEstradaObject(EstradaAudit, pbversion) as EstradaAudit;
}
