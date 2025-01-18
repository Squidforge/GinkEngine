import { Model } from "../../model";
import { View } from "../../core/view";
export class ActionView extends View {
    static __name__ = "ActionView";
}
export class Action extends Model {
    static __name__ = "Action";
    static __module__ = "bokeh.models.dom";
    constructor(attrs) {
        super(attrs);
    }
}
//# sourceMappingURL=action.js.map