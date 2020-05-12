import { Projection } from "../../../protobuf/roads_pb";

import { projToWGS84, toDms, toUtm } from "../crsUtilities";
import { makeEstradaObject } from "../protoBufUtilities";

export class EstradaProjection extends Projection {
    get x() {
        return this.getX();
    }

    get y() {
        return this.getY();
    }

    get dms() {
        return toDms(projToWGS84.forward(projectionToCoordinates(this)));
    }

    get utm() {
        return toUtm(projToWGS84.forward(projectionToCoordinates(this)));
    }
}

function projectionToCoordinates(
    proj: Projection | EstradaProjection): [number, number] {
    return [proj.getX(), proj.getY()];
}

export function makeEstradaProjection(pbprojection: { [name: string]: any }): EstradaProjection {
    return makeEstradaObject(EstradaProjection, pbprojection) as EstradaProjection;
}
