import { ToggleButtonGroup, ToggleButtonGroupView } from "./toggle_button_group";
import * as buttons from "../../styles/buttons.css";
export class RadioButtonGroupView extends ToggleButtonGroupView {
    static __name__ = "RadioButtonGroupView";
    change_active(i) {
        if (this.model.active !== i) {
            this.model.active = i;
        }
    }
    _update_active() {
        const { active } = this.model;
        this._buttons.forEach((button_el, i) => {
            button_el.classList.toggle(buttons.active, active === i);
        });
    }
}
export class RadioButtonGroup extends ToggleButtonGroup {
    static __name__ = "RadioButtonGroup";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = RadioButtonGroupView;
        this.define(({ Int, Nullable }) => ({
            active: [Nullable(Int), null],
        }));
    }
}
//# sourceMappingURL=radio_button_group.js.map