import { Version } from "../../../protobuf/roads_pb";

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
}

export function getFieldName(field) {
    return (auditSchema[field]) ? auditSchema[field].display : "";
}

export function getHelpText(field) {
    return (auditSchema[field]) ? auditSchema[field].help_text : "";
}
