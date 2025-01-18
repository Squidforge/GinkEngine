import { Tool, ToolView } from "../tool";
import { ClickButton } from "../click_button";
import { Signal } from "../../../core/signaling";
export class ActionToolView extends ToolView {
    static __name__ = "ActionToolView";
    connect_signals() {
        super.connect_signals();
        this.connect(this.model.do, (arg) => this.doit(arg));
    }
}
export class ActionTool extends Tool {
    static __name__ = "ActionTool";
    constructor(attrs) {
        super(attrs);
    }
    do = new Signal(this, "do");
    tool_button() {
        return new ClickButton({ tool: this });
    }
}
//# sourceMappingURL=action_tool.js.map