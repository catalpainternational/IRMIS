import { Version } from "../protobuf/roads_pb";

const auditSchema = {
    id: { display: "Id" },
    dateCreated: { display: "Date" },
    user: { display: "User" },
    comment: { display: "Description" },
};

export class EstradaAudit extends Version {
    getId() {
        return this.getPk();
    }

    get id() {
        return this.getPk();
    }

    get dateCreated() {
        return this.hasDateCreated() ? this.getDateCreated() : undefined;
    }

    get user() {
        return this.getUser();
    }

    get comment() {
        return this.getComment();
    }
}

export function getFieldName(field) {
    return (auditSchema[field]) ? auditSchema[field].display : "";
}

export function getHelpText(field) {
    return (auditSchema[field]) ? auditSchema[field].help_text : "";
}
