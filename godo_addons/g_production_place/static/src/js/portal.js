odoo.define('g_production_place.portal', function(require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    const Dialog = require('web.Dialog');
    const { _t, qweb } = require('web.core');
    const ajax = require('web.ajax');
    const session = require('web.session');

    publicWidget.registry.portalDetails = publicWidget.Widget.extend({
        selector: '.o_portal_details',
        events: {
            'change select[name="province_id"]': '_onProvinceChange', 
        },

        /**
         * @override
         */
        start: function() {
            var def = this._super.apply(this, arguments);

            this.$district = this.$('select[name="district_id"]');
            this.$districtOptions = this.$district.filter(':enabled').find('option:not(:first)');
            this._adaptAddressForm();

            return def;
        },

        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * @private
         */
        _adaptAddressForm: function() {
            var $province = this.$('select[name="province_id"]');
            var provinceID = ($province.val() || 0);
            this.$districtOptions.detach();
            var $displayedDistrict = this.$districtOptions.filter('[data-province_id=' + provinceID + ']');
            var nb = $displayedDistrict.appendTo(this.$district).show().length;
            this.$district.parent().toggle(nb >= 1);
        },

        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------

        /**
         * @private
         */
        _onProvinceChange: function() {
            this._adaptAddressForm();
        },
    });

    publicWidget.registry.portalDetails = publicWidget.Widget.extend({
        selector: '.o_portal_my_home',
        events: {
            'click button[id="btn-add-position"]': '_onAddLatLng', 
            'click button[id="btn-add-farmer"]': '_onAddFarmer', 
        },

        /**
         * @override
         */
        start: function() {
            var def = this._super.apply(this, arguments);
            this.$latlngWrapper = this.$('div[id="latlng"]');
            this.$farmerWrapper = this.$('div[id="farmer"]'); 

            return def;
        },

        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * @private
         */
         _onAddLatLng: function() { 
            var _latInput = `<input type="number" class="form-control" />`
            var _lngInput = `<input type="number" class="form-control" />`
            $(`<div class="row"><div class="col-6">${_latInput}</div><div class="col-6">${_lngInput}</div></div>`).appendTo(this.$latlngWrapper)
        },

        _onAddFarmer: function() { 
            var index = this.$farmerWrapper.length+1
            var _index = `<input type="number" class="form-control" value="${index}" disabled />`
            var _farmerName = `<input type="number" class="form-control" placeholder="Tên nông hộ" />`
            var _farmArea = `<input type="number" class="form-control" placeholder="Tên nông hộ"/>`
            $(`<div class="row"><div class="col-2">${_index}</div><div class="col-6">${_farmerName}</div><div class="col-6">${_farmArea}</div></div>`).appendTo(this.$farmerWrapper)
        },

        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------

        /**
         * @private
         */
        _onProvinceChange: function() {
            this._adaptAddressForm();
        },
    });

  
    publicWidget.registry.PortalHomeCounters = publicWidget.Widget.extend({
        selector: '.o_portal_my_home',

        /**
         * @override
         */
        start: function() {
            var def = this._super.apply(this, arguments);
            this._updateCounters();
            return def;
        },

        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * @private
         */
        async _updateCounters(elem) {
            const numberRpc = 3;
            const needed = this.$('[data-placeholder_count]')
                .map((i, o) => $(o).data('placeholder_count'))
                .toArray();
            const counterByRpc = Math.ceil(needed.length / numberRpc); // max counter, last can be less

            const proms = [...Array(Math.min(numberRpc, needed.length)).keys()].map(async i => {
                await this._rpc({
                    route: "/my/counters",
                    params: {
                        counters: needed.slice(i * counterByRpc, (i + 1) * counterByRpc)
                    },
                }).then(data => {
                    Object.keys(data).map(k => this.$("[data-placeholder_count='" + k + "']").text(data[k]));
                });
            });
            return Promise.all(proms);
        },
    });

    publicWidget.registry.portalSearchPanel = publicWidget.Widget.extend({
        selector: '.o_portal_search_panel',
        events: {
            'click .dropdown-item': '_onDropdownItemClick',
            'submit': '_onSubmit',
        },

        /**
         * @override
         */
        start: function() {
            var def = this._super.apply(this, arguments);
            this._adaptSearchLabel(this.$('.dropdown-item.active'));
            return def;
        },

        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * @private
         */
        _adaptSearchLabel: function(elem) {
            var $label = $(elem).clone();
            $label.find('span.nolabel').remove();
            this.$('input[name="search"]').attr('placeholder', $label.text().trim());
        },
        /**
         * @private
         */
        _search: function() {
            var search = $.deparam(window.location.search.substring(1));
            search['search_in'] = this.$('.dropdown-item.active').attr('href').replace('#', '');
            search['search'] = this.$('input[name="search"]').val();
            window.location.search = $.param(search);
        },

        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------

        /**
         * @private
         */
        _onDropdownItemClick: function(ev) {
            ev.preventDefault();
            var $item = $(ev.currentTarget);
            $item.closest('.dropdown-menu').find('.dropdown-item').removeClass('active');
            $item.addClass('active');

            this._adaptSearchLabel(ev.currentTarget);
        },
        /**
         * @private
         */
        _onSubmit: function(ev) {
            ev.preventDefault();
            this._search();
        },
    });

    publicWidget.registry.NewAPIKeyButton = publicWidget.Widget.extend({
        selector: '.o_portal_new_api_key',
        events: {
            click: '_onClick'
        },

        async _onClick(e) {
            e.preventDefault();
            // This call is done just so it asks for the password confirmation before starting displaying the
            // dialog forms, to mimic the behavior from the backend, in which it asks for the password before
            // displaying the wizard.
            // The result of the call is unused. But it's required to call a method with the decorator `@check_identity`
            // in order to use `handleCheckIdentity`.
            await handleCheckIdentity(this.proxy('_rpc'), this._rpc({
                model: 'res.users',
                method: 'api_key_wizard',
                args: [session.user_id],
            }));
            await ajax.loadXML('/portal/static/src/xml/portal_security.xml', qweb);
            const self = this;
            const d_description = new Dialog(self, {
                title: _t('New API Key'),
                $content: qweb.render('portal.keydescription'),
                buttons: [{
                    text: _t('Confirm'),
                    classes: 'btn-primary',
                    close: true,
                    click: async() => {
                        var description = d_description.el.querySelector('[name="description"]').value;
                        var wizard_id = await this._rpc({
                            model: 'res.users.apikeys.description',
                            method: 'create',
                            args: [{ name: description }],
                        });
                        var res = await handleCheckIdentity(
                            this.proxy('_rpc'),
                            this._rpc({
                                model: 'res.users.apikeys.description',
                                method: 'make_key',
                                args: [wizard_id],
                            })
                        );
                        const d_show = new Dialog(self, {
                            title: _t('API Key Ready'),
                            $content: qweb.render('portal.keyshow', { key: res.context.default_key }),
                            buttons: [{ text: _t('Close'), clases: 'btn-primary', close: true }],
                        });
                        d_show.on('closed', this, () => {
                            window.location = window.location;
                        });
                        d_show.open();
                    }
                }, { text: _t('Discard'), close: true }],
            });
            d_description.opened(() => {
                const input = d_description.el.querySelector('[name="description"]');
                input.focus();
                d_description.el.addEventListener('submit', (e) => {
                    e.preventDefault();
                    d_description.$footer.find('.btn-primary').click();
                });
            });
            d_description.open();
        }
    });

    publicWidget.registry.RemoveAPIKeyButton = publicWidget.Widget.extend({
        selector: '.o_portal_remove_api_key',
        events: {
            click: '_onClick'
        },

        async _onClick(e) {
            e.preventDefault();
            await handleCheckIdentity(
                this.proxy('_rpc'),
                this._rpc({
                    model: 'res.users.apikeys',
                    method: 'remove',
                    args: [parseInt(this.target.id)]
                })
            );
            window.location = window.location;
        }
    });

    /**
     * Wraps an RPC call in a check for the result being an identity check action
     * descriptor. If no such result is found, just returns the wrapped promise's
     * result as-is; otherwise shows an identity check dialog and resumes the call
     * on success.
     *
     * Warning: does not in and of itself trigger an identity check, a promise which
     * never triggers and identity check internally will do nothing of use.
     *
     * @param {Function} rpc Widget#_rpc bound do the widget
     * @param {Promise} wrapped promise to check for an identity check request
     * @returns {Promise} result of the original call
     */
    function handleCheckIdentity(rpc, wrapped) {
        return wrapped.then((r) => {
            if (!_.isMatch(r, { type: 'ir.actions.act_window', res_model: 'res.users.identitycheck' })) {
                return r;
            }
            const check_id = r.res_id;
            return ajax.loadXML('/portal/static/src/xml/portal_security.xml', qweb).then(() => new Promise((resolve, reject) => {
                const d = new Dialog(null, {
                    title: _t("Security Control"),
                    $content: qweb.render('portal.identitycheck'),
                    buttons: [{
                        text: _t("Confirm Password"),
                        classes: 'btn btn-primary',
                        // nb: if click & close, waits for click to resolve before closing
                        click() {
                            const password_input = this.el.querySelector('[name=password]');
                            if (!password_input.reportValidity()) {
                                password_input.classList.add('is-invalid');
                                return;
                            }
                            return rpc({
                                model: 'res.users.identitycheck',
                                method: 'write',
                                args: [check_id, { password: password_input.value }]
                            }).then(() => rpc({
                                model: 'res.users.identitycheck',
                                method: 'run_check',
                                args: [check_id]
                            })).then((r) => {
                                this.close();
                                resolve(r);
                            }, (err) => {
                                err.event.preventDefault(); // suppress crashmanager
                                password_input.classList.add('is-invalid');
                                password_input.setCustomValidity(_t("Check failed"));
                                password_input.reportValidity();
                            });
                        }
                    }, {
                        text: _t('Cancel'),
                        close: true
                    }]
                }).on('close', null, () => {
                    // unlink wizard object?
                    reject();
                });
                d.opened(() => {
                    const pw = d.el.querySelector('[name="password"]');
                    pw.focus();
                    pw.addEventListener('input', () => {
                        pw.classList.remove('is-invalid');
                        pw.setCustomValidity('');
                    });
                    d.el.addEventListener('submit', (e) => {
                        e.preventDefault();
                        d.$footer.find('.btn-primary').click();
                    });
                });
                d.open();
            }));
        });
    }
    return {
        handleCheckIdentity,
    }
});