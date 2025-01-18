import { DOMView } from "../../core/dom_view";
import { Model } from "../../model";
export class DOMNodeView extends DOMView {
    static __name__ = "DOMNodeView";
}
export class DOMNode extends Model {
    static __name__ = "DOMNode";
    static __module__ = "bokeh.models.dom";
    constructor(attrs) {
        super(attrs);
    }
}
//# sourceMappingURL=dom_node.js.map