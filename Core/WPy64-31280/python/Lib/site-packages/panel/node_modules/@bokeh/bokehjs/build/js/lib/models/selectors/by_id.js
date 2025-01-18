import { Selector } from "./selector";
export class ByID extends Selector {
    static __name__ = "ByID";
    constructor(attrs) {
        super(attrs);
    }
    find_one(target) {
        return target.querySelector(`#${this.query}`);
    }
}
//# sourceMappingURL=by_id.js.map