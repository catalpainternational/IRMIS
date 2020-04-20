import * as L from "leaflet";
// tslint:disable: max-line-length

/** A sample of various baselayers - we'll likely choose one of the OSM - Open Street Map - sources */
export class BaseLayers {
    private static mapDataAttribution = 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors';
    private static mapCCv3Attribution = '<a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>';

    private static mapboxAccessToken = "pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw";
    private static mapboxUrlTemplate = `https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=${BaseLayers.mapboxAccessToken}`;
    private static mapboxLayerOptions = {
        attribution: BaseLayers.mapDataAttribution + ", " +
            '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
            'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id: "mapbox.satellite",
        maxZoom: 18,
    };

    private static mapStamenAttribution = 'Map tiles by <a href="http://stamen.com">Stamen Design</a>';
    private static stamenWatercolorUrlTemplate = "https://stamen-tiles-{s}.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.{ext}";
    private static stamenWatercolorLayerOptions = {
        attribution: BaseLayers.mapStamenAttribution + ", " + BaseLayers.mapCCv3Attribution +
            " &mdash; " + BaseLayers.mapDataAttribution,
        ext: "jpg",
        maxZoom: 16,
        minZoom: 1,
        subdomains: "abcd",
    };

    // Has problems with national boundary placement at zoom 9 and above (smaller)
    private static stamenTerrainUrlTemplate = "https://stamen-tiles-{s}.a.ssl.fastly.net/terrain-background/{z}/{x}/{y}{r}.{ext}";
    private static stamenTerrainLayerOptions = {
        attribution: BaseLayers.mapStamenAttribution + ", " + BaseLayers.mapCCv3Attribution +
            " &mdash; " + BaseLayers.mapDataAttribution,
        ext: "png",
        maxZoom: 18,
        minZoom: 1,
        subdomains: "abcd",
    };

    // Yuck - awful at the zoom levels we need
    private static openTopoUrlTemplate = "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png";
    private static openTopoLayerOptions = {
        attribution: BaseLayers.mapDataAttribution + ", " +
            '<a href="http://viewfinderpanoramas.org">SRTM</a> | ' +
            'Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
        maxZoom: 17,
    };

    private static osmMapnikUrlTemplate = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
    private static osmMapnikLayerOptions = {
        attribution: "&copy; " + BaseLayers.mapDataAttribution,
        maxZoom: 19,
    };

    private static osmHOTUrlTemplate = "https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png";
    private static osmHOTLayerOptions = {
        attribution: "&copy; " + BaseLayers.mapDataAttribution + ", " +
            'hosted by <a href="https://openstreetmap.fr/" target="_blank">OpenStreetMap France</a>',
        maxZoom: 19,
    };

    private static esriWorldImageryUrlTemplate = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}";
    private static esriWorldImageryLayerOptions = {
        attribution: "Tiles &copy; Esri &mdash; " +
            "Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community",
    };

    private static thunderforestAccessToken = "a3c846cef468496cb5759eff6b05136a";
    private static spinalMapUrlTemplate = `https://tile.thunderforest.com/spinal-map/{z}/{x}/{y}.png?apikey=${BaseLayers.thunderforestAccessToken}`;
    private static spinalMapUrlLayerOptions = {
        attribution: "Maps &copy; <a href='https://www.thunderforest.com'>Thunderforest</a>, " + BaseLayers.mapDataAttribution,
    };

    public static get baseLayers() {
        const mapbox = L.tileLayer(BaseLayers.mapboxUrlTemplate, BaseLayers.mapboxLayerOptions);
        const stamenWatercolor = L.tileLayer(BaseLayers.stamenWatercolorUrlTemplate, BaseLayers.stamenWatercolorLayerOptions);
        const stamenTerrain = L.tileLayer(BaseLayers.stamenTerrainUrlTemplate, BaseLayers.stamenTerrainLayerOptions);
        const openTopo = L.tileLayer(BaseLayers.openTopoUrlTemplate, BaseLayers.openTopoLayerOptions);
        const osmMapnik = L.tileLayer(BaseLayers.osmMapnikUrlTemplate, BaseLayers.osmMapnikLayerOptions);
        const osmHOT = L.tileLayer(BaseLayers.osmHOTUrlTemplate, BaseLayers.osmHOTLayerOptions);
        const esriWorldImagery = L.tileLayer(BaseLayers.esriWorldImageryUrlTemplate, BaseLayers.esriWorldImageryLayerOptions);
        const spinalMap = L.tileLayer(BaseLayers.spinalMapUrlTemplate, BaseLayers.spinalMapUrlLayerOptions);

        // tslint:disable: object-literal-sort-keys
        return {
            "Terrain": stamenTerrain,
            "Topographic": openTopo,
            "Street OSM Mapnik": osmMapnik,
            "Street OSM HOT": osmHOT,
            "Satellite Mapbox": mapbox,
            "Satellite Esri": esriWorldImagery,
            "Watercolor": stamenWatercolor,
            "<span onmouseover='this.innerHTML=\"SpinalMap\"' onmouseout='this.innerHTML=\"&nbsp;&nbsp;&nbsp;\"'>&nbsp;&nbsp;&nbsp;</span>": spinalMap,
        } as {[key: string]: any};
    }
}
