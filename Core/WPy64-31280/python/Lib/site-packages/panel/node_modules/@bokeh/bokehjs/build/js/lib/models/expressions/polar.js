import { CoordinateTransform } from "../expressions/coordinate_transform";
import { Direction } from "../../core/enums";
import * as p from "../../core/properties";
export class PolarTransform extends CoordinateTransform {
    static __name__ = "PolarTransform";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({}) => ({
            radius: [p.DistanceSpec, { field: "radius" }],
            angle: [p.AngleSpec, { field: "angle" }],
            direction: [Direction, "anticlock"],
        }));
    }
    _v_compute(source) {
        const radius = this.properties.radius.uniform(source);
        const angle = this.properties.angle.uniform(source);
        const coeff = this.direction == "anticlock" ? -1 : 1;
        const n = Math.min(radius.length, angle.length);
        const x = new Float64Array(n);
        const y = new Float64Array(n);
        for (let i = 0; i < n; i++) {
            const radius_i = radius.get(i);
            const angle_i = angle.get(i) * coeff;
            x[i] = radius_i * Math.cos(angle_i);
            y[i] = radius_i * Math.sin(angle_i);
        }
        return { x, y };
    }
}
//# sourceMappingURL=polar.js.map