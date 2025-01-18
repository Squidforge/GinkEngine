import { PlotActionTool, PlotActionToolView } from "./plot_action_tool";
import { tool_icon_redo } from "../../../styles/icons.css";
export class RedoToolView extends PlotActionToolView {
    static __name__ = "RedoToolView";
    connect_signals() {
        super.connect_signals();
        this.connect(this.plot_view.state.changed, () => this.model.disabled = !this.plot_view.state.can_redo);
    }
    doit() {
        const state = this.plot_view.state.redo();
        if (state?.range != null) {
            this.plot_view.trigger_ranges_update_event();
        }
    }
}
export class RedoTool extends PlotActionTool {
    static __name__ = "RedoTool";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = RedoToolView;
        this.override({
            disabled: true,
        });
        this.register_alias("redo", () => new RedoTool());
    }
    tool_name = "Redo";
    tool_icon = tool_icon_redo;
}
//# sourceMappingURL=redo_tool.js.map