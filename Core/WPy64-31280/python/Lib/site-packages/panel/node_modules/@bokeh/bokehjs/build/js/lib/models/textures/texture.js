import { Model } from "../../model";
import { TextureRepetition } from "../../core/enums";
export class Texture extends Model {
    static __name__ = "Texture";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(() => ({
            repetition: [TextureRepetition, "repeat"],
        }));
    }
}
//# sourceMappingURL=texture.js.map