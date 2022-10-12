odoo.define('g_production_place.puc_map', function(require) {
    "use strict";

    const AbstractAction = require('web.AbstractAction');
    const core = require('web.core');
    const config = require('web.config');
    var ajax = require('web.ajax');
    var map;
    var polyLayers = [];


    const MapAction = AbstractAction.extend({
        template: 'puc_map_container',
        xmlDependencies: ['/g_production_place/static/src/xml/puc_map.xml'],
        init: function(parent, action) {
            this._super.apply(this, arguments);
            // this.url = _.str.sprintf("/report/barcode/?type=QR&value=%s&width=256&height=256&humanreadable=1", action.params.url);

            setTimeout(() => {
                var mapDom = document.getElementById('map')
                if (mapDom) {
                    map = L.map('map').setView([21.004136, 105.864864], 12);
                    L.tileLayer('https://maps.vnpost.vn/api/tm/{z}/{x}/{y}@2x.png?apikey=8fb3246c12d442525034be04bcd038f22e34571be4adbd4c', {
                        maxZoom: 18,
                        minZoom: 6,
                        attribution: '© SmartLife'
                    }).addTo(map);

                    // console.log(mapDom, '=>trong')

                    ajax.jsonRpc("/web/puc/coordinates", 'call', {}).then(function(res) {
                        var drawnItems = new L.FeatureGroup();
                        map.addLayer(drawnItems);
                        res.forEach(item => {
                            let polygon = L.polygon(item.coordinates);
                            polygon.setStyle({ fillColor: '#46832f', color: '#46832f', fillOpacity: 0.5, weight: 1 });
                            polygon.bindPopup(` <div class="card" style="border-radius: 12px;">
                            <div class="card-header popup-header bg-primary">
                                <h2 class="m-0">${item.name} (${item.code})</h2>
                            </div>
                            <div class="card-body">
                                <div class="row mx-0 py-1">
                                    <div class="col-6"> Mã số: ${item.code} </div>
                                    <div class="col-6"> Diện tích: ${item.area} </div>
                                </div>
                                <div class="row mx-0 py-1">
                                    <div class="col-6"> Loại cây trồng: ${item.tree} </div>
                                    <div class="col-6"> Thị trường xuất khẩu: ${item.export_to} </div>
                                </div>
                                <div class="row mx-0 py-1">
                                    <div class="col-6"> Sản lượng hàng năm (tấn): ${item.years_average_production} </div>
                                    <div class="col-6"> Số nông hộ: ${item.plant_farm_num} </div>
                                </div>
                                <div class="row mx-0 py-1">
                                    <div class="col-6"> Đơn vị sở hữu: ${item.registered_owner} </div>
                                    <div class="col-6"> Địa chỉ: ${item.registered_owner_address} </div>
                                </div>
                                <div class="row mx-0 py-1">
                                    <div class="col-12"> Danh sách nông hộ:</div>
                                    <div class="col-12">${item.farmers} </div>
                                </div>
                            </div>
                        </div>`)
                            drawnItems.addLayer(polygon);
                        });

                        console.log(res)
                    });

                }

                console.log(mapDom)

            }, 500)

        },
        start: () => {



        }
    });

    core.action_registry.add('puc_map', MapAction);
});