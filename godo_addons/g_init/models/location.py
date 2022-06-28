from odoo import models, fields, _

class ResProvince(models.Model):
    _name = 'res.province'
    _description = _('Province')

    name = fields.Char(string='Tên tỉnh', required=True)
    province_code = fields.Char(string='Mã tỉnh' , required=True)

class ResDistrict(models.Model):
    _name = 'res.district'
    _description = _('District')

    name = fields.Char(string='Tên huyện', required=True)
    district_code = fields.Char(string='Mã Huyện', required=True)
    parent_code = fields.Char(string="Mã tỉnh", required=True)
    depend_province = fields.Many2one('res.province', string='Thuộc tỉnh', required=True)
     

class ResWard(models.Model):
    _name ='res.ward'
    _description = _('Ward')

    name = fields.Char(string='Tên xã', required=True)
    ward_code = fields.Char(string="Mã xã", required=True)
    parent_code = fields.Char(string='Mã huyện', required=True)
    depend_district = fields.Many2one('res.district',string='Thuộc huyện', required=True)
    depend_province = fields.Many2one(related='depend_district.depend_province',string='Thuộc tỉnh', readonly=True, required=True)