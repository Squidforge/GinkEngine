import { Model } from "../../model";
import { Selection } from "../selections/selection";
export class DataSource extends Model {
    static __name__ = "DataSource";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ Ref }) => ({
            selected: [Ref(Selection), () => new Selection(), { readonly: true }],
        }));
    }
}
//# sourceMappingURL=data_source.js.map