from odoo import models, fields, api, _

class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description =  _('Tờ khai vùng trồng')