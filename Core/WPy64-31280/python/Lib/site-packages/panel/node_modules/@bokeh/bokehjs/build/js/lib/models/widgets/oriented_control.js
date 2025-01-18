import { Control, ControlView } from "./control";
import { Orientation } from "../../core/enums";
export class OrientedControlView extends ControlView {
    static __name__ = "OrientedControlView";
}
export class OrientedControl extends Control {
    static __name__ = "OrientedControl";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(() => ({
            orientation: [Orientation, "horizontal"],
        }));
    }
}
//# sourceMappingURL=oriented_control.js.map