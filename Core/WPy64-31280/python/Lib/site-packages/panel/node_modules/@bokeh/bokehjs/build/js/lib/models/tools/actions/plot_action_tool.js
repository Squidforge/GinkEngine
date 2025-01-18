import { ActionTool, ActionToolView } from "./action_tool";
export class PlotActionToolView extends ActionToolView {
    static __name__ = "PlotActionToolView";
    get plot_view() {
        return this.parent;
    }
}
export class PlotActionTool extends ActionTool {
    static __name__ = "PlotActionTool";
    constructor(attrs) {
        super(attrs);
    }
}
//# sourceMappingURL=plot_action_tool.js.map