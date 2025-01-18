import { Selector } from "./selector";
export class ByXPath extends Selector {
    static __name__ = "ByXPath";
    constructor(attrs) {
        super(attrs);
    }
    find_one(target) {
        return document.evaluate(this.query, target).iterateNext();
    }
}
//# sourceMappingURL=by_xpath.js.map