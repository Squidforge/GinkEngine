import { Markup, MarkupView } from "./markup";
import { pre } from "../../core/dom";
export class PreTextView extends MarkupView {
    static __name__ = "PreTextView";
    render() {
        super.render();
        const content = pre({ style: { overflow: "auto" } }, this.model.text);
        this.markup_el.appendChild(content);
    }
}
export class PreText extends Markup {
    static __name__ = "PreText";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = PreTextView;
    }
}
//# sourceMappingURL=pretext.js.map