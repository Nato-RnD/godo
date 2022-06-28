from odoo import models, fields, api,_

class HrEmployee(models.Model): 
    _inherit = 'hr.employee'
    
    
    province_id = fields.Many2one(comodel_name='res.province', string='Tỉnh/Thành')
    district_id = fields.Many2one(comodel_name='res.district', string='Huyện/Quận')
    ward_id = fields.Many2one(comodel_name='res.province', string='Xã/Phường')