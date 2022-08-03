#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class GodoProductionUnitDeclaration(models.Model):
    _name = 'godo.production.unit.declaration'
    _description =  _('Tờ khai vùng trồng')

    name = fields.Char(string='Tên vùng trồng')
    address = fields.Char('Địa chỉ')
    plant_id = fields.Many2one(comodel_name='godo.production.item',string='Loại cây trồng')
    export_to = fields.Many2one(comodel_name='res.country',string='Thị trường xuất khẩu')
    annual_harvest_time = fields.Integer(string='Số lần thu hoạch/năm')
    area = fields.Float(string='Diện tích')
    plant_farm_num = fields.Integer(string='Số nông hộ')
    three_years_average_production = fields.Float('Sản lượng tấn/ha/năm')

    registered_owner_name = fields.Char(string='Tổ chức/cá nhân đăng ký')
    registered_owner_type= fields.Selection(selection=[('personal','Cá nhân'),('company','Tổ chức/Doanh nghiệp')], default='company' ,required=True, string='Loại hình hoạt động')
    registered_owner_representer = fields.Char(string='Đại diện')
    registered_owner_address = fields.Char(string='Địa chỉ liên hệ')
    registered_owner_code = fields.Char(string='Mã số DN/CCCD')
    phone = fields.Char(string='Điện thoại')
    fax = fields.Char(string='Fax')
    email = fields.Char(string='Email')
    has_vietgap_global_gap = fields.Boolean(string='Có chứng nhận Viet Gap, Global Gap')

class GodoProductionUnitInspection(models.Model):
    _name = 'godo.production.unit.inspection'
    _description = _('Biên bản kiểm tra')

    name = fields.Char('Tên')
    