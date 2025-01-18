import { ToolButton, ToolButtonView } from "./tool_button";
export class ClickButtonView extends ToolButtonView {
    static __name__ = "ClickButtonView";
    _clicked() {
        this.model.tool.do.emit(undefined);
    }
}
export class ClickButton extends ToolButton {
    static __name__ = "ClickButton";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = ClickButtonView;
    }
}
//# sourceMappingURL=click_button.js.map