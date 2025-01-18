export class Diagnostics {
    static __name__ = "Diagnostics";
    listeners = new Set();
    connect(listener) {
        this.listeners.add(listener);
    }
    disconnect(listener) {
        this.listeners.delete(listener);
    }
    report(obj) {
        for (const listener of this.listeners) {
            listener(obj);
        }
    }
}
export const diagnostics = new Diagnostics();
//# sourceMappingURL=diagnostics.js.map