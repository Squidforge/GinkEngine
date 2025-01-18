import { buffer_to_base64 } from "../util/buffer";
import { equals } from "../util/eq";
export class Buffer {
    buffer;
    static __name__ = "Buffer";
    constructor(buffer) {
        this.buffer = buffer;
    }
    to_base64() {
        return buffer_to_base64(this.buffer);
    }
    [equals](that, cmp) {
        return cmp.eq(this.buffer, that.buffer);
    }
}
export class Base64Buffer extends Buffer {
    static __name__ = "Base64Buffer";
    toJSON() {
        return this.to_base64();
    }
}
//# sourceMappingURL=buffer.js.map