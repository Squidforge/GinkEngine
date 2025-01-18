import { Selector } from "./selector";
export class ByClass extends Selector {
    static __name__ = "ByClass";
    constructor(attrs) {
        super(attrs);
    }
    find_one(target) {
        return target.querySelector(`.${this.query}`);
    }
}
//# sourceMappingURL=by_class.js.map