import { ContinuousAxis, ContinuousAxisView } from "./continuous_axis";
import { BasicTickFormatter } from "../formatters/basic_tick_formatter";
import { BasicTicker } from "../tickers/basic_ticker";
export class LinearAxisView extends ContinuousAxisView {
    static __name__ = "LinearAxisView";
}
export class LinearAxis extends ContinuousAxis {
    static __name__ = "LinearAxis";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = LinearAxisView;
        this.override({
            ticker: () => new BasicTicker(),
            formatter: () => new BasicTickFormatter(),
        });
    }
}
//# sourceMappingURL=linear_axis.js.map