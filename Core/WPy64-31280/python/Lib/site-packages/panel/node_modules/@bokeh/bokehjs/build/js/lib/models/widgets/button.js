import { AbstractButton, AbstractButtonView } from "./abstract_button";
import { ButtonClick } from "../../core/bokeh_events";
export class ButtonView extends AbstractButtonView {
    static __name__ = "ButtonView";
    click() {
        this.model.trigger_event(new ButtonClick());
        super.click();
    }
}
export class Button extends AbstractButton {
    static __name__ = "Button";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = ButtonView;
        this.override({
            label: "Button",
        });
    }
    on_click(callback) {
        this.on_event(ButtonClick, callback);
    }
}
//# sourceMappingURL=button.js.map