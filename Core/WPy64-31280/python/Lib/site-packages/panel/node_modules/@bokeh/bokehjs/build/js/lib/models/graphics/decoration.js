import { Marking } from "./marking";
import { Model } from "../../model";
import { View } from "../../core/view";
import { build_view } from "../../core/build_views";
export class DecorationView extends View {
    static __name__ = "DecorationView";
    visuals;
    marking;
    *children() {
        yield* super.children();
        yield this.marking;
    }
    async lazy_initialize() {
        await super.lazy_initialize();
        this.marking = await build_view(this.model.marking, { parent: this.parent });
    }
}
export class Decoration extends Model {
    static __name__ = "Decoration";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = DecorationView;
        this.define(({ Enum, Ref }) => ({
            marking: [Ref(Marking)],
            node: [Enum("start", "middle", "end")],
        }));
    }
}
//# sourceMappingURL=decoration.js.map