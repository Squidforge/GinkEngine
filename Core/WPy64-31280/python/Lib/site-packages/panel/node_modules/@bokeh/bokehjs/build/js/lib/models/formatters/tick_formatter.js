import { Model } from "../../model";
import { TextBox } from "../../core/graphics";
export class TickFormatter extends Model {
    static __name__ = "TickFormatter";
    constructor(attrs) {
        super(attrs);
    }
    format_graphics(ticks, opts) {
        return this.doFormat(ticks, opts).map((text) => new TextBox({ text }));
    }
    compute(tick, opts) {
        return this.doFormat([tick], opts ?? { loc: 0 })[0];
    }
    v_compute(tick, opts) {
        return this.doFormat(tick, opts ?? { loc: 0 });
    }
}
//# sourceMappingURL=tick_formatter.js.map