from odoo import models, fields, api, _

class ResCountry(models.Model):
    _inherit = 'res.country'

    target_country = fields.Boolean('Là thị trường mục tiêu')