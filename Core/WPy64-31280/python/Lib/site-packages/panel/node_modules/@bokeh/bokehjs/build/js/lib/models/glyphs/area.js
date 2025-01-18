import { Glyph, GlyphView } from "./glyph";
import { generic_area_scalar_legend } from "./utils";
import * as mixins from "../../core/property_mixins";
export class AreaView extends GlyphView {
    static __name__ = "AreaView";
    draw_legend_for_index(ctx, bbox, _index) {
        generic_area_scalar_legend(this.visuals, ctx, bbox);
    }
}
export class Area extends Glyph {
    static __name__ = "Area";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.mixins([mixins.FillScalar, mixins.HatchScalar]);
    }
}
//# sourceMappingURL=area.js.map