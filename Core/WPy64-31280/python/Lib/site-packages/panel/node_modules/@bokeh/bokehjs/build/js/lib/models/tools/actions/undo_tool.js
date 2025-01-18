import { PlotActionTool, PlotActionToolView } from "./plot_action_tool";
import { tool_icon_undo } from "../../../styles/icons.css";
export class UndoToolView extends PlotActionToolView {
    static __name__ = "UndoToolView";
    connect_signals() {
        super.connect_signals();
        this.connect(this.plot_view.state.changed, () => this.model.disabled = !this.plot_view.state.can_undo);
    }
    doit() {
        const state = this.plot_view.state.undo();
        if (state?.range != null) {
            this.plot_view.trigger_ranges_update_event();
        }
    }
}
export class UndoTool extends PlotActionTool {
    static __name__ = "UndoTool";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = UndoToolView;
        this.override({
            disabled: true,
        });
        this.register_alias("undo", () => new UndoTool());
    }
    tool_name = "Undo";
    tool_icon = tool_icon_undo;
}
//# sourceMappingURL=undo_tool.js.map