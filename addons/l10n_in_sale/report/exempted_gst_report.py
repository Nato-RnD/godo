# -*- coding: utf-8 -*-
# Part of Godo. See LICENSE file for full copyright and licensing details.

from odoo import models


class L10nInExemptedReport(models.Model):
    _inherit = "l10n_in.exempted.report"

    def _from(self):
        from_str = super(L10nInExemptedReport, self)._from()
        from_str += """ AND aml.product_id != COALESCE(
            (SELECT value from ir_config_parameter where key = 'sale.default_deposit_product_id'), '0')::int
            """
        return from_str
