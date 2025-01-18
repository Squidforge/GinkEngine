import { PlotActionTool, PlotActionToolView } from "./plot_action_tool";
import { tool_icon_reset } from "../../../styles/icons.css";
export class ResetToolView extends PlotActionToolView {
    static __name__ = "ResetToolView";
    doit() {
        // reset() issues the RangesUpdate event
        this.plot_view.reset();
    }
}
export class ResetTool extends PlotActionTool {
    static __name__ = "ResetTool";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = ResetToolView;
        this.register_alias("reset", () => new ResetTool());
    }
    tool_name = "Reset";
    tool_icon = tool_icon_reset;
}
//# sourceMappingURL=reset_tool.js.map