#-*- coding: utf-8 -*- 
from odoo import models, fields, api, _
import uuid
class GodoProductionUnitDeclaration(models.Model):
    _name = 'godo.production.unit.declaration'
    _description =  _('Tờ khai vùng trồng')
    
    _STATE_SELECTIONS = [
        ('draft',_('Nháp')),
        ('post',_('Đã đăng ký')),
        ('done', _('Đã duyệt')),
        ('rejected',_('Đã từ chối')),
        ('cancelled',_('Đã hủy'))
    ]

    name = fields.Char(string='Tên vùng trồng', required=True)
    address = fields.Char('Địa chỉ')
    tree_id = fields.Many2one(comodel_name='godo.production.item',string='Loại cây trồng')
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
    farm_ids = fields.Many2many(comodel_name='res.partner',relation='godo_production_unit_declaration_farm_rel', column1='declaration_id', column2='farm_id', string='Danh sách các hộ nông dân')
    certificate_attachment_ids = fields.Many2many(comodel_name='ir.attachment',relation='godo_production_unit_declaration_certification_attachment_rel', column1='declaration_id', column2='attachment_id', string='Bản sao chứng nhận')
    agreement_attachment_ids = fields.Many2many(comodel_name='ir.attachment',relation='godo_production_unit_declaration_agreement_attachment_rel', column1='declaration_id', column2='attachment_id', string='Cam kết')
    map_kml_id = fields.Binary(string='Bản đồ (file KML)')
    form_uuid = fields.Char(string='Mã đăng ký', 
        compute='_form_uuid_gen', store=True )
    state = fields.Selection(selection=_STATE_SELECTIONS,default='draft',string='Trạng thái')
    @api.depends('name')
    def _form_uuid_gen(self):
        for record in self:
            if record.id is None:
                record.form_uuid = uuid.uuid4().hex
    
    
class GodoProductionUnitCode(models.Model):
    _name = 'godo.production.unit.code'
    _description = _('Mã số vùng trồng')
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _STATE_SELECTIONS = [ 
        ('active',_('Đang sử dụng')),
        ('suspend', _('Tạm dừng')), 
        ('cancelled',_('Đã hủy'))
    ]
    name = fields.Char('Tên vùng trồng')
    code = fields.Char('Mã số vùng trồng')
    declaration_id = fields.Many2one(comodel_name='godo.production.unit.declaration', string='Mẫu khai báo')
    address = fields.Char('Địa chỉ')
    tree_id = fields.Many2one(comodel_name='godo.production.item',string='Loại cây trồng')
    export_to = fields.Many2one(comodel_name='res.country',string='Thị trường xuất khẩu')
    annual_harvest_time = fields.Integer(string='Số lần thu hoạch/năm')
    area = fields.Float(string='Diện tích')
    plant_farm_num = fields.Integer(string='Số nông hộ')
    three_years_average_production = fields.Float('Sản lượng tấn/ha/năm')

    registered_owner_id = fields.Many2one(comodel_name='res.partner', string='Tổ chức/cá nhân đăng ký')
    registered_owner_type= fields.Selection(selection=[('personal','Cá nhân'),('company','Tổ chức/Doanh nghiệp')], default='company' ,required=True, string='Loại hình hoạt động')
    registered_owner_representer = fields.Char(string='Đại diện')
    registered_owner_address = fields.Char(string='Địa chỉ liên hệ')
    registered_owner_code = fields.Char(string='Mã số DN/CCCD')
    phone = fields.Char(string='Điện thoại')
    fax = fields.Char(string='Fax')
    email = fields.Char(string='Email')
    has_vietgap_global_gap = fields.Boolean(string='Có chứng nhận Viet Gap, Global Gap')
    map_kml = fields.Binary('Bản đồ (file KML)')
    state = fields.Selection(selection=_STATE_SELECTIONS,default='active',string='Trạng thái')
    



class GodoProductionUnitInspection(models.Model):
    _name = 'godo.production.unit.inspection' 
    _description = _('Biên bản kiểm tra')
    _inherit = ['mail.thread', 'mail.activity.mixin']

    STATE_SELECTIONS = [
        ('draft','Nháp'),
        ('post','Đã ghi nhận'),
        ('approved','Đã duyệt')
    ]

    name = fields.Char('Tên biên bản kiểm tra'),
    checker_id = fields.Many2one(comodel_name='res.users', string='Người kiểm tra')
    job_position = fields.Char('Chức vụ')
    registered_owner_id = fields.Many2one(comodel_name='res.partner', string='Tổ chức/cá nhân đăng ký')
    production_place = fields.Char('Tên vùng trồng')
    production_place_address = fields.Char('Địa chỉ vùng trồng')
    tree_id = fields.Many2one(comodel_name='godo.production.item',string='Loại cây trồng')
    export_to = fields.Many2one(comodel_name='res.country',string='Thị trường xuất khẩu')


    #Thong tin vung trong
    production_unit_area = fields.Float('Diện tích')
    plant_farm_num = fields.Integer(string='Số nông hộ')
    tree_age = fields.Integer('Tuổi cây')
    growth_stage = fields.Char('Giai đoạn sinh trưởng')
    harvest_time = fields.Char('Thời gian dự kiến thu hoạch')
    expected_production = fields.Float('Sản lượng dự kiến')
    # Giong cay trong
    tree_seed_id  = fields.Many2one(comodel_name='godo.production.seed', string='Giống cây trồng')
    #Thuoc bao ve thuc vat
    vn_allowed_pesticides_ids = fields.Many2many(comodel_name='godo.material.pesticides', relation='godo_production_unit_inspection_pesticides_rel', column1='inspection_id', column2='pesticides_id',string='Thuốc BVTV Vn cho phép')
    import_country_allowed_pesticides_ids = fields.Many2many(comodel_name='godo.material.pesticides', relation='godo_production_unit_inspection_pesticides_rel', column1='inspection_id', column2='pesticides_id',string='Thuốc BVTV nước nhập khẩu cho phép')
    other_pesticides_ids =  fields.Many2many(comodel_name='godo.material.pesticides', relation='godo_production_unit_inspection_pesticides_rel', column1='inspection_id', column2='pesticides_id',string='Thuốc BVTV khác')
    
    has_plant_diary = fields.Boolean('Sổ nhật ký canh tác')
    has_fully_note = fields.Char('Ghi chép đầy đủ')
    additional_note = fields.Char('Ghi chép bổ sung')
    pest_composition_density = fields.Char('Thành phần và mật độ sinh vật gây hại')
    pest_anti_applying_method = fields.Char('Phương pháp quản lý')
    has_sampling = fields.Boolean('Lấy mẫu')
    sampling_report = fields.Binary('Kết quả lấy mẫu')
    has_farming_certificate = fields.Char('Áp dụng thực hành sản xuất tốt')
    no_wild_grass = fields.Boolean('Sạch cỏ dại, tàn dư thực vật')
    pesticides_pack_clearance = fields.Char('Dọn dẹp thu gom bao bì')
    has_note = fields.Boolean('Có ghi chép thông tin')
    other_item = fields.Text('Các nội dung khác')
    conclusion = fields.Text('Kết luận')
    state = fields.Selection(selection=STATE_SELECTIONS, default='draft', string='Trạng thái')

    #https://drive.google.com/file/d/1mO1Xhc1a8vaCVNRdOjHTUv_iZ0hJw4jO/view