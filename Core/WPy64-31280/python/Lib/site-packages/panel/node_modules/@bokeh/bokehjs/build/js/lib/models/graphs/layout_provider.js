import { Model } from "../../model";
import { CoordinateTransform } from "../expressions/coordinate_transform";
export class LayoutProvider extends Model {
    static __name__ = "LayoutProvider";
    constructor(attrs) {
        super(attrs);
    }
    get node_coordinates() {
        return new NodeCoordinates({ layout: this });
    }
    get edge_coordinates() {
        return new EdgeCoordinates({ layout: this });
    }
}
export class GraphCoordinates extends CoordinateTransform {
    static __name__ = "GraphCoordinates";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ Ref }) => ({
            layout: [Ref(LayoutProvider)],
        }));
    }
}
export class NodeCoordinates extends GraphCoordinates {
    static __name__ = "NodeCoordinates";
    constructor(attrs) {
        super(attrs);
    }
    _v_compute(source) {
        const [x, y] = this.layout.get_node_coordinates(source);
        return { x, y };
    }
}
export class EdgeCoordinates extends GraphCoordinates {
    static __name__ = "EdgeCoordinates";
    constructor(attrs) {
        super(attrs);
    }
    _v_compute(source) {
        const [x, y] = this.layout.get_edge_coordinates(source);
        return { x, y };
    }
}
//# sourceMappingURL=layout_provider.js.map