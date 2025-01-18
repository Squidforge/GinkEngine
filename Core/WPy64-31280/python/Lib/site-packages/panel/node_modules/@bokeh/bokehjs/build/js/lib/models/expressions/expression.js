import { Model } from "../../model";
export class Expression extends Model {
    static __name__ = "Expression";
    constructor(attrs) {
        super(attrs);
    }
    _result;
    initialize() {
        super.initialize();
        this._result = new Map();
    }
    v_compute(source) {
        let result = this._result.get(source);
        if (result === undefined || source.changed_for(this)) {
            result = this._v_compute(source);
            this._result.set(source, result);
        }
        return result;
    }
}
export class ScalarExpression extends Model {
    static __name__ = "ScalarExpression";
    constructor(attrs) {
        super(attrs);
    }
    _result;
    initialize() {
        super.initialize();
        this._result = new Map();
    }
    compute(source) {
        let result = this._result.get(source);
        if (result === undefined || source.changed_for(this)) {
            result = this._compute(source);
            this._result.set(source, result);
        }
        return result;
    }
}
//# sourceMappingURL=expression.js.map