# -*- coding: utf-8 -*-
# Part of Godo. See LICENSE file for full copyright and licensing details.


def _preserve_tag_on_taxes(cr, registry):
    from odoo.addons.account.models.chart_template import preserve_existing_tags_on_taxes
    preserve_existing_tags_on_taxes(cr, registry, 'l10n_pl')
