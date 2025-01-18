import { Renderer, RendererView } from "./renderer";
import { auto_ranged } from "../ranges/data_range1d";
export class DataRendererView extends RendererView {
    static __name__ = "DataRendererView";
    get xscale() {
        return this.coordinates.x_scale;
    }
    get yscale() {
        return this.coordinates.y_scale;
    }
    [auto_ranged] = true;
    bounds() {
        return this.glyph_view.bounds();
    }
    log_bounds() {
        return this.glyph_view.log_bounds();
    }
}
export class DataRenderer extends Renderer {
    static __name__ = "DataRenderer";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.override({
            level: "glyph",
        });
    }
    get selection_manager() {
        return this.get_selection_manager();
    }
}
//# sourceMappingURL=data_renderer.js.map