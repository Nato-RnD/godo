# -*- coding: utf-8 -*-
# Part of Godo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class StockInventoryWarning(models.TransientModel):
    _name = 'stock.inventory.warning'
    _description = 'Inventory Adjustment Warning'

    quant_ids = fields.Many2many('stock.quant')

    def action_reset(self):
        return self.quant_ids.action_set_inventory_quantity_to_zero()

    def action_set(self):
        valid_quants = self.quant_ids.filtered(lambda quant: not quant.inventory_quantity_set)
        return valid_quants.action_set_inventory_quantity()
