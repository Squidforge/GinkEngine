import { ContinuousAxis, ContinuousAxisView } from "./continuous_axis";
import { DatetimeTickFormatter } from "../formatters/datetime_tick_formatter";
import { DatetimeTicker } from "../tickers/datetime_ticker";
export class DatetimeAxisView extends ContinuousAxisView {
    static __name__ = "DatetimeAxisView";
}
export class DatetimeAxis extends ContinuousAxis {
    static __name__ = "DatetimeAxis";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = DatetimeAxisView;
        this.override({
            ticker: () => new DatetimeTicker(),
            formatter: () => new DatetimeTickFormatter(),
        });
    }
}
//# sourceMappingURL=datetime_axis.js.map