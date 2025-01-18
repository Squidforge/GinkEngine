import { Tool, ToolView } from "../tool";
import { OnOffButton } from "../on_off_button";
export class GestureToolView extends ToolView {
    static __name__ = "GestureToolView";
    get plot_view() {
        return this.parent;
    }
}
export class GestureTool extends Tool {
    static __name__ = "GestureTool";
    constructor(attrs) {
        super(attrs);
    }
    tool_button() {
        return new OnOffButton({ tool: this });
    }
}
//# sourceMappingURL=gesture_tool.js.map