odoo.define('g_production_place.puc_map', function(require) {
    "use strict";

    const AbstractAction = require('web.AbstractAction');
    const core = require('web.core');
    const config = require('web.config');

    const MapAction = AbstractAction.extend({
        template: 'puc_map_container',
        xmlDependencies: ['/g_production_place/static/src/xml/puc_map.xml'],

        init: function(parent, action) {
            this._super.apply(this, arguments);
            this.url = _.str.sprintf("/report/barcode/?type=QR&value=%s&width=256&height=256&humanreadable=1", action.params.url);

            setTimeout(() => {
                var mapDom = document.getElementById('map')
                if (mapDom) {
                    var map = L.map('map').setView([51.505, -0.09], 13);
                    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                        maxZoom: 19,
                        attribution: '© OpenStreetMap'
                    }).addTo(map);

                    console.log(mapDom, '=>trong')
                }

                console.log(mapDom)

            }, 500)

        },
        start: () => {

        }
    });

    core.action_registry.add('puc_map', MapAction);
});