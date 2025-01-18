import { FlexBox, FlexBoxView } from "./flex_box";
export class RowView extends FlexBoxView {
    static __name__ = "RowView";
    _direction = "row";
}
export class Row extends FlexBox {
    static __name__ = "Row";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = RowView;
    }
}
//# sourceMappingURL=row.js.map