import { Version } from "../protobuf/roads_pb";

import { getFieldName, getHelpText } from "./assets/protoBufUtilities";

const auditSchema = {
    id: { display: "Id" },
    dateCreated: { display: gettext("Date") },
    user: { display: gettext("User") },
    comment: { display: gettext("Description") },
};

export class EstradaAudit extends Version {
    getId() {
        return this.getPk();
    }

    get id() {
        return this.getPk();
    }

    get dateCreated() {
        return this.hasDateCreated() ? new Date(this.getDateCreated().getSeconds() * 1000) : undefined;
    }

    get user() {
        return this.getUser();
    }

    get comment() {
        return this.getComment();
    }
        
    static getFieldName(field) {
        return getFieldName(auditSchema, field);
    }

    static getHelpText(field) {
        return getHelpText(auditSchema, field);
    }
}
