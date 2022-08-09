odoo.define('g_logistic.bill_search', function(require) {
    var PublicWidget = require('web.public.widget');
    var rpc = require('web.rpc');
    var core = require('web.core');
    var QWeb = core.qweb;
    var BillSearch = PublicWidget.Widget.extend({
        selector: '.dynamic_snippet_blog',
        xmlDependencies: ['/g_logistic/static/src/xml/search.xml'],
        start: function() {
            var self = this;
            self.$('#btn-bill-search').on('click', () => {
                let _code = self.$('#txt-bill-search').val()
                if (_code === '' || _code === undefined) {
                    return {
                        'type': 'ir.actions.client',
                        'tag': 'action_warn',
                        'name': 'Warning',
                        'params': {
                            'title': 'Warning!',
                            'text': 'Vui lòng nhập mã vận đơn',
                            'sticky': true
                        }
                    }
                }

                rpc.query({
                    route: '/bill-search',
                    params: { code: _code },
                }).then(function(result) {
                    self.$('#search-result').html(QWeb.render('BillSearch.Result', { 'search_result': result }))

                });
            })
        },
    });
    PublicWidget.registry.dynamic_snippet_blog = BillSearch;
    return BillSearch;
});