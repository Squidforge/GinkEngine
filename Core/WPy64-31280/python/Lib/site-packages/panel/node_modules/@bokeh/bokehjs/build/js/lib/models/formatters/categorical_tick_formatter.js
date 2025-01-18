import { TickFormatter } from "./tick_formatter";
import { copy } from "../../core/util/array";
export class CategoricalTickFormatter extends TickFormatter {
    static __name__ = "CategoricalTickFormatter";
    constructor(attrs) {
        super(attrs);
    }
    doFormat(ticks, _opts) {
        return copy(ticks);
    }
}
//# sourceMappingURL=categorical_tick_formatter.js.map