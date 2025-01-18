import { Renderer, RendererView } from "./renderer";
export class GuideRendererView extends RendererView {
    static __name__ = "GuideRendererView";
}
export class GuideRenderer extends Renderer {
    static __name__ = "GuideRenderer";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.override({
            level: "guide",
        });
    }
}
//# sourceMappingURL=guide_renderer.js.map