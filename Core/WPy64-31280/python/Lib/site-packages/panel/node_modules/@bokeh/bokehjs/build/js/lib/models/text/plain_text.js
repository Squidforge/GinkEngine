import { BaseText, BaseTextView } from "./base_text";
import { TextBox } from "../../core/graphics";
export class PlainTextView extends BaseTextView {
    static __name__ = "PlainTextView";
    initialize() {
        super.initialize();
        this._has_finished = true;
    }
    graphics() {
        return new TextBox({ text: this.model.text });
    }
}
export class PlainText extends BaseText {
    static __name__ = "PlainText";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = PlainTextView;
    }
}
//# sourceMappingURL=plain_text.js.map