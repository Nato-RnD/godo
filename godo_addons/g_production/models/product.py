#-*- coding: utf-8 -*-

from odoo import models, fields, api 

class GodoProductionProduct(models.Model):
    _inherit = 'product.product'
    _description = 'Sản phẩm'
    # state = fields.Selection(selection=[('draft','Nháp'),('done','Đang sử dụng'),('cancelled','Đã hủy')],   index=True, tracking=3, default='draft', string='Trạng thái') 