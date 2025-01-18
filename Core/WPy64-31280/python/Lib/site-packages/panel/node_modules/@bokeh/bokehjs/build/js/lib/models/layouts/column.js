import { FlexBox, FlexBoxView } from "./flex_box";
export class ColumnView extends FlexBoxView {
    static __name__ = "ColumnView";
    _direction = "column";
}
export class Column extends FlexBox {
    static __name__ = "Column";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = ColumnView;
    }
}
//# sourceMappingURL=column.js.map