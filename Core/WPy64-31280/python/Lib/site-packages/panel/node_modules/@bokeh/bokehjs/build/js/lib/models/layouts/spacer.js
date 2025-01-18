import { LayoutDOM, LayoutDOMView } from "./layout_dom";
export class SpacerView extends LayoutDOMView {
    static __name__ = "SpacerView";
    get child_models() {
        return [];
    }
    _auto_width = "auto";
    _auto_height = "auto";
}
export class Spacer extends LayoutDOM {
    static __name__ = "Spacer";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = SpacerView;
    }
}
//# sourceMappingURL=spacer.js.map