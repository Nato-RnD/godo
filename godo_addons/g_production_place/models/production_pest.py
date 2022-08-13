#-*- coding: utf-8 -*- 
from odoo import models, fields, api, _

class GodoProductionPest(models.Model):
    _name = 'godo.production.pest'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description =  _('Sinh vật có hại')

    name = fields.Char(string='Tên gọi')
    image = fields.Image(string='Hình ảnh')
    tree_id = fields.Many2one(comodel_name='godo.production.item', string='Loại cây')
    description = fields.Text(string='Mô tả')
