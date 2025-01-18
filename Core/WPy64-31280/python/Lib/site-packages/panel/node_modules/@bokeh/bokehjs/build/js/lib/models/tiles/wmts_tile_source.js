import { MercatorTileSource } from "./mercator_tile_source";
export class WMTSTileSource extends MercatorTileSource {
    static __name__ = "WMTSTileSource";
    constructor(attrs) {
        super(attrs);
    }
    get_image_url(x, y, z) {
        const image_url = this.string_lookup_replace(this.url, this.extra_url_vars);
        const [wx, wy, wz] = this.tms_to_wmts(x, y, z);
        return image_url
            .replace("{X}", wx.toString())
            .replace("{Y}", wy.toString())
            .replace("{Z}", wz.toString());
    }
}
//# sourceMappingURL=wmts_tile_source.js.map