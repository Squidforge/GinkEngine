import { XYGlyph, XYGlyphView } from "./xy_glyph";
import { LineVector, FillVector, HatchVector } from "../../core/property_mixins";
import * as p from "../../core/properties";
export class CenterRotatableView extends XYGlyphView {
    static __name__ = "CenterRotatableView";
    get max_w2() {
        return this.model.properties.width.units == "data" ? this.max_width / 2 : 0;
    }
    get max_h2() {
        return this.model.properties.height.units == "data" ? this.max_height / 2 : 0;
    }
    _bounds({ x0, x1, y0, y1 }) {
        const { max_w2, max_h2 } = this;
        return {
            x0: x0 - max_w2,
            x1: x1 + max_w2,
            y0: y0 - max_h2,
            y1: y1 + max_h2,
        };
    }
}
export class CenterRotatable extends XYGlyph {
    static __name__ = "CenterRotatable";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.mixins([LineVector, FillVector, HatchVector]);
        this.define(({}) => ({
            angle: [p.AngleSpec, 0],
            width: [p.DistanceSpec, { field: "width" }],
            height: [p.DistanceSpec, { field: "height" }],
        }));
    }
}
//# sourceMappingURL=center_rotatable.js.map