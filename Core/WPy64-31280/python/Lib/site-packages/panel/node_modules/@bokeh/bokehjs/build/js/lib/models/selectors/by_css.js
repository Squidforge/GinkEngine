import { Selector } from "./selector";
export class ByCSS extends Selector {
    static __name__ = "ByCSS";
    constructor(attrs) {
        super(attrs);
    }
    find_one(target) {
        return target.querySelector(this.query);
    }
}
//# sourceMappingURL=by_css.js.map