import { Widget, WidgetView } from "./widget";
import { toggle_attribute } from "../../core/dom";
export class ControlView extends WidgetView {
    static __name__ = "ControlView";
    connect_signals() {
        super.connect_signals();
        this.connect(this.disabled, (disabled) => {
            for (const el of this.controls()) {
                toggle_attribute(el, "disabled", disabled);
            }
        });
    }
}
export class Control extends Widget {
    static __name__ = "Control";
    constructor(attrs) {
        super(attrs);
    }
}
//# sourceMappingURL=control.js.map