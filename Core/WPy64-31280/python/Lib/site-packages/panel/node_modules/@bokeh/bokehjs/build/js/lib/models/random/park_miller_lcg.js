import { RandomGenerator } from "./random_generator";
import { LCGRandom } from "../../core/util/random";
export class ParkMillerLCG extends RandomGenerator {
    static __name__ = "ParkMillerLCG";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.define(({ Int, Nullable }) => ({
            seed: [Nullable(Int), null],
        }));
    }
    generator() {
        return new LCGRandom(this.seed ?? Date.now());
    }
}
//# sourceMappingURL=park_miller_lcg.js.map