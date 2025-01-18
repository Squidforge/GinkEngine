import { ToolButton, ToolButtonView } from "./tool_button";
import * as tools from "../../styles/tool_button.css";
export class OnOffButtonView extends ToolButtonView {
    static __name__ = "OnOffButtonView";
    _toggle_active() {
        this.class_list.toggle(tools.active, this.model.tool.active);
    }
    connect_signals() {
        super.connect_signals();
        const { active } = this.model.tool.properties;
        this.on_change(active, () => {
            this._toggle_active();
        });
    }
    render() {
        super.render();
        this._toggle_active();
    }
    _clicked() {
        const { active } = this.model.tool;
        this.model.tool.active = !active;
    }
}
export class OnOffButton extends ToolButton {
    static __name__ = "OnOffButton";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = OnOffButtonView;
    }
}
//# sourceMappingURL=on_off_button.js.map