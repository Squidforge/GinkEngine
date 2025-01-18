import { DOMElement, DOMElementView } from "./dom_element";
export class SpanView extends DOMElementView {
    static __name__ = "SpanView";
    static tag_name = "span";
}
export class Span extends DOMElement {
    static __name__ = "Span";
    static {
        this.prototype.default_view = SpanView;
    }
}
export class DivView extends DOMElementView {
    static __name__ = "DivView";
    static tag_name = "div";
}
export class Div extends DOMElement {
    static __name__ = "Div";
    static {
        this.prototype.default_view = DivView;
    }
}
export class TableView extends DOMElementView {
    static __name__ = "TableView";
    static tag_name = "table";
}
export class Table extends DOMElement {
    static __name__ = "Table";
    static {
        this.prototype.default_view = TableView;
    }
}
export class TableRowView extends DOMElementView {
    static __name__ = "TableRowView";
    static tag_name = "tr";
}
export class TableRow extends DOMElement {
    static __name__ = "TableRow";
    static {
        this.prototype.default_view = TableRowView;
    }
}
//# sourceMappingURL=elements.js.map