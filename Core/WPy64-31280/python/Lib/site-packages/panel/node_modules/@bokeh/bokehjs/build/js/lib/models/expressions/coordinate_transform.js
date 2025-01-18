import { Expression } from "../expressions/expression";
export class CoordinateTransform extends Expression {
    static __name__ = "CoordinateTransform";
    constructor(attrs) {
        super(attrs);
    }
    get x() {
        return new XComponent({ transform: this });
    }
    get y() {
        return new YComponent({ transform: this });
    }
}
export class XYComponent extends Expression {
    static __name__ = "XYComponent";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ Ref }) => ({
            transform: [Ref(CoordinateTransform)],
        }));
    }
}
export class XComponent extends XYComponent {
    static __name__ = "XComponent";
    constructor(attrs) {
        super(attrs);
    }
    _v_compute(source) {
        return this.transform.v_compute(source).x;
    }
}
export class YComponent extends XYComponent {
    static __name__ = "YComponent";
    constructor(attrs) {
        super(attrs);
    }
    _v_compute(source) {
        return this.transform.v_compute(source).y;
    }
}
//# sourceMappingURL=coordinate_transform.js.map