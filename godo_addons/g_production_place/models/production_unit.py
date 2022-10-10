#-*- coding: utf-8 -*- 
from odoo import models, fields, api, _
import uuid
class GodoProductionUnitDeclaration(models.Model):
    _name = 'godo.production.unit.declaration'
    _description =  _('Tờ khai vùng trồng')
    _inherit =['mail.thread', 'mail.activity.mixin'] 
    
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
    registered_user_id = fields.Many2one(comodel_name='res.users', string='Người dùng')
    registered_owner_name = fields.Char(string='Tổ chức/cá nhân đăng ký')
    registered_owner_type= fields.Selection(selection=[('personal','Cá nhân'),('company','Tổ chức/Doanh nghiệp')], default='company' ,required=True, string='Loại hình hoạt động')
    registered_owner_representer = fields.Char(string='Đại diện')
    registered_owner_address = fields.Char(string='Địa chỉ liên hệ')
    registered_owner_code = fields.Char(string='Mã số DN/CCCD')
    
    phone = fields.Char(string='Điện thoại')
    fax = fields.Char(string='Fax')
    email = fields.Char(string='Email')
    has_vietgap_global_gap = fields.Boolean(string='Có chứng nhận Viet Gap, Global Gap')
    # farm_ids = fields.Many2many(comodel_name='res.partner',relation='godo_production_unit_declaration_farm_rel', column1='declaration_id', column2='farm_id', string='Danh sách các hộ nông dân')
    farmers = fields.Text(string='Danh sách các hộ nông dân')
    certificate_attachment_ids = fields.Many2many(comodel_name='ir.attachment',relation='godo_production_unit_declaration_certification_attachment_rel', column1='declaration_id', column2='attachment_id', string='Bản sao chứng nhận')
    agreement_attachment_ids = fields.Many2many(comodel_name='ir.attachment',relation='godo_production_unit_declaration_agreement_attachment_rel', column1='declaration_id', column2='attachment_id', string='Cam kết')
    map_kml_id = fields.Binary(string='Bản đồ (file KML)')
    coordinates = fields.Text('Tọa độ địa lý')
    form_uuid = fields.Char(string='Mã đăng ký', 
        compute='_form_uuid_gen', store=True )
    inspection_ids = fields.One2many(comodel_name='godo.production.unit.inspection', inverse_name='declaration_id', string='Danh sách Biên bản kiểm tra')
    has_inspection = fields.Boolean(string='Đã lập biên bản', compute='_has_inspection_compute', store=True)
    state = fields.Selection(selection=_STATE_SELECTIONS,default='draft',string='Trạng thái')

    @api.depends('inspection_ids')
    def _has_inspection_compute(self):
        self.ensure_one()
        if len(self.inspection_ids)>0:
            self.has_inspection = True

    @api.depends('name')
    def _form_uuid_gen(self):
        for record in self:
            if record.id is None:
                record.form_uuid = uuid.uuid4().hex

    def puc_declaration_post(self):
        self.ensure_one()
        self.state = 'post'
        self.message_post(body= _('%s đã đăng ký vùng trồng %s' % (self.env.user.name or self.registered_owner_name, self.name) ))

    def puc_declaration_inspection(self):
        self.ensure_one() 
        return {
        'name': _('Biên bản kiểm tra'),
        'view_type': 'form',
        'view_mode': 'form',
        # 'view_id': self.env.ref('production_place_management_inspection_form_view').read()[0],
        'res_model': 'godo.production.unit.inspection',
        'type': 'ir.actions.act_window',
        'target': 'current',
                'context': {
                    'activated': self.id
                }
        }
        
    def puc_declaration_code_issue(self):
        self.ensure_one()
        # self.state = 'done'
        # self.message_post(body= _('%s đã cấp mã số vùng trồng %s' % (self.env.user.name or self.registered_owner_name, self.name) ))
        
        return {
        'name': _('Mã vùng trồng'),
        'view_type': 'form',
        'view_mode': 'form', 
        'res_model': 'godo.production.unit.code',
        'type': 'ir.actions.act_window',
        'target': 'current',
                'context': {
                    'activated': self.id
                }
        }


    @api.model
    def default_get(self, default_fields):
        res = super(GodoProductionUnitDeclaration, self).default_get(default_fields)  
 
        
        return res

        # self.state = 'post'
        # self.message_post(body= _('%s đã đăng ký vùng trồng %s' % (self.user_id.name, self.name) ))
    
    
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
    farmers = fields.Text(string='Danh sách các hộ nông dân')
    coordinates = fields.Text('Tọa độ địa lý') 
    state = fields.Selection(selection=_STATE_SELECTIONS,default='draft',string='Trạng thái')
    
    
    def _puc_issue(self, **kw):
        pass
    
    @api.model
    def default_get(self, default_fields):

        _active_id =  self.env.context.get('active_id')
 
        _declaration = self.env['godo.production.unit.declaration'].browse(_active_id)
        res = super(GodoProductionUnitCode, self).default_get(default_fields) 
        res['name'] = _declaration.name
        res['code'] = 'VN'
        res['address'] = _declaration.address
        res['tree_id'] = _declaration.tree_id.id
        res['declaration_id'] = _active_id
        return res



class GodoProductionUnitInspection(models.Model):
    _name = 'godo.production.unit.inspection' 
    _description = _('Biên bản kiểm tra')
    _inherit = ['mail.thread', 'mail.activity.mixin']

    STATE_SELECTIONS = [
        ('draft','Nháp'),
        ('ready','Xác nhận'),
        ('post','Đã báo cáo'),
        ('approved','Đã duyệt')
    ]

    name = fields.Char('Tên biên bản kiểm tra ')
    declaration_id = fields.Many2one(comodel_name='godo.production.unit.declaration', string='Mẫu khai báo')
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

    def puc_inspection_ready(self):
        self.ensure_one()
        self.state = 'ready'
        self.message_post(body= _('%s đã xác nhận %s' % (self.checker_id.name, self.name) ))
         

    def puc_inspection_post(self):
        self.ensure_one()
        self.state = 'post'
        self.message_post(body= _('%s đã lập báo cáo kết quả kiểm tra vùng trồng %s' % (self.checker_id.name, self.production_place) ))

    def puc_inspection_draft(self):
        self.ensure_one()
        self.state = 'draft'
        self.message_post(body= _('%s đã chuyển trạng thái thành bản nháp %s' % (self.checker_id.name, self.name) ))

    def puc_declaration_issue_code(self):
        self.ensure_one()
        self.state = 'approved'
        self.message_post(body= _('%s đã cấp mã số cho vùng trồng %s' % (self.checker_id.name, self.production_place) ))

    def puc_inspection_export_report(self):
        pass

    @api.model
    def default_get(self, default_fields):

        _active_id =  self.env.context.get('active_id')
 
        _declaration = self.env['godo.production.unit.declaration'].browse(_active_id)
        res = super(GodoProductionUnitInspection, self).default_get(default_fields) 
        res['name'] = _declaration.name
        res['declaration_id'] = _active_id
        return res
       
        