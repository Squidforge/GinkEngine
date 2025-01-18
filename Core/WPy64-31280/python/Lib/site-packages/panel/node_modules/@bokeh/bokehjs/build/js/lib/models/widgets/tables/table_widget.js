import { Widget } from "../widget";
import { ColumnDataSource } from "../../sources/column_data_source";
import { CDSView } from "../../sources/cds_view";
export class TableWidget extends Widget {
    static __name__ = "TableWidget";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ Ref }) => ({
            source: [Ref(ColumnDataSource), () => new ColumnDataSource()],
            view: [Ref(CDSView), () => new CDSView()],
        }));
    }
}
//# sourceMappingURL=table_widget.js.map