odoo.define('smart_customers.dashboard', function(require) {
    'use strict';

    var core = require('web.core');
    var Context = require('web.Context');
    var AbstractAction = require('web.AbstractAction');
    var Dialog = require('web.Dialog');
    var datepicker = require('web.datepicker');
    var session = require('web.session');
    var field_utils = require('web.field_utils');
    var RelationalFields = require('web.relational_fields');
    var StandaloneFieldManagerMixin = require('web.StandaloneFieldManagerMixin');
    var WarningDialog = require('web.CrashManager').WarningDialog;
    var Widget = require('web.Widget'); 
    var QWeb = core.qweb;
    var _t = core._t;

    var buildingDashboardWidget = AbstractAction.extend({
        hasControlPanel: true,

        events: {
            'input .o_bms_building_filter_input': 'filter_accounts',
            'click .o_bms_building_summary': 'edit_summary',
            'click .js_building_dashboard_save_summary': 'save_summary',
            'click .o_bms_building_footnote_icons': 'delete_footnote',
            'click .js_bms_building_add_footnote': 'add_edit_footnote',
            'click .js_building_dashboard_foldable': 'fold_unfold',
            'click [action]': 'trigger_action',
            'click .o_bms_building_load_more span': 'load_more',
            'click .o_bms_building_table thead th': 'selected_column',
            'click .o_change_expected_date': '_onChangeExpectedDate',

        },

        custom_events: {
            'value_changed': function(ev) {
                var self = this;
                console.log('Kong hieu sao')
                    // self.report_options.partner_ids = ev.data.partner_ids;
                    // self.report_options.partner_categories = ev.data.partner_categories;
                    // self.report_options.analytic_accounts = ev.data.analytic_accounts;
                    // self.report_options.analytic_tags = ev.data.analytic_tags;
                return self.reload().then(function() {
                    self.$searchview_buttons.find('#building_selected').change()
                        // self.$searchview_buttons.find('.account_partner_filter').click();
                        // self.$searchview_buttons.find('.account_analytic_filter').click();
                });
            },
        },

        init: function(parent, action) {
            this.actionManager = parent;
            this.report_model = action.context.model;
            if (this.report_model === undefined) {
                this.report_model = 'res.account';
            }
            this.financial_id = false;
            if (action.context.id) {
                this.financial_id = action.context.id;
            }
            this.odoo_context = action.context;
            this.report_options = action.options || false;
            this.ignore_session = action.ignore_session;
            // if ((action.ignore_session === 'read' || action.ignore_session === 'both') !== true) {
            //     var persist_key = 'report:' + this.report_model + ':' + this.financial_id + ':' + session.company_id;
            //     this.report_options = JSON.parse(sessionStorage.getItem(persist_key)) || this.report_options;
            // }
            return this._super.apply(this, arguments);
        },
        start: function() {
            var self = this;
            var extra_info = this._rpc({
                    model: self.report_model,
                    method: 'overview_dashboard',
                    args: [null, null],
                    kwargs: { 'building': null, 'block': null },
                    context: self.odoo_context,
                })
                .then(function(result) {
                    return self.parse_reports_informations(result);
                });
            return Promise.all([extra_info, this._super.apply(this, arguments)]).then(function() {
                self.render();
            });
            // return Promise.all([])
        },
        parse_reports_informations: function(values) {
            this.report_options = values.options;
            this.odoo_context = values.context;
            this.report_manager_id = values.report_manager_id;
            // this.footnotes = values.footnotes;
            // this.buttons = values.buttons;
            // this.headers = values.header_html;
            this.header_title = values.header_title;
            this.html = values.html;
            this.$searchview_buttons = $(values.header_html);
            // this.$searchview_buttons = $(values.searchview_html);
            // this.persist_options();
        },

        do_show: function() {
            this._super.apply(this, arguments);
            this.update_cp();
        },
        // Updates the control panel and render the elements that have yet to be rendered
        update_cp: function() {
            var status = {
                cp_content: {
                    $buttons: $(`<h2>${this.header_title}</h2>`),
                    $pager: this.$pager,
                    // $searchview: this.$searchview,
                    $searchview_buttons: this.$searchview_buttons
                },
            };
            console.log(status, this.headers)
            return this.updateControlPanel(status, { clear: true });
        },
        reload: function() {
            var self = this;
            return this._rpc({
                    model: self.report_model,
                    method: 'get_building_infomation',
                    args: [self.building, self.block],
                    kwargs: { 'building': self.building, 'block': self.block },
                    context: self.odoo_context,
                })
                .then(function(result) {
                    self.parse_reports_informations(result);
                    return self.render();
                });


        },
        render: function() {
            // var self = this;
            this.render_template();
            this.readerHeaders();
            this.update_cp();
        },
        render_template: function() {
            this.$('.o_content').html(this.html);
        },

        readerHeaders: function() {
            var self = this
            this.$headers = $(QWeb.render("buildingDashboard.buttons", { headers: this.header_html }));

            $(function() {
                $("[data-toggle=popover]").popover({
                    html: true,
                    placement: 'top',
                    content: function() {
                        var content = $(this).attr("data-popover-content");
                        return $(content).children(".popover-body").html();
                    },
                    title: function() {
                        var title = $(this).attr("data-popover-content");
                        return $(title).children(".popover-heading").html();
                    },
                });


                getDetail = (id) => {
                    self.do_action({
                        type: 'ir.actions.act_window',
                        name: _t('Flat Detail'),
                        target: 'new',
                        res_id: id,
                        res_model: 'bms.flat',
                        views: [
                            [false, 'form']
                        ],
                        flags: {
                            mode: 'readonly'
                        }
                    });
                }
            });




            this.$searchview_buttons.find('#building_selected').change(() => {
                let _building = $("select[id=building_selected] option:selected").val()
                let _block = null
                self.setBuildingBlock(_building, _block)
                self.reload()
            })

            this.$searchview_buttons.find('#block_selected').change(() => {
                let _building = $("select[id=building_selected] option:selected").val()
                let _block = $("select[id=block_selected] option:selected").val()
                self.setBuildingBlock(_building, _block)
                self.reload()
            })



            return this.$headers
        },

        setBuildingBlock: function(building, block) {
            this.building = building
            this.block = block
        }

    });

    core.action_registry.add('dashboard', buildingDashboardWidget);

    return buildingDashboardWidget;

});


getDetail = (id) => {}

