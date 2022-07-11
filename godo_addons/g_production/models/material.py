#-*- coding: utf-8 -*-  
from odoo import SUPERUSER_ID, models, fields, api, tools
from odoo.exceptions import UserError, ValidationError

class GodoMaterialFertilizerCategory(models.Model):
    _name = 'godo.material.fertilizer.category'
    _description = 'Fertilizer Category'   
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = 'complete_name'
    _order = 'complete_name'

    name = fields.Char('Tên nhóm', index=True, required=True)
    complete_name = fields.Char(
        'Tên nhóm', compute='_compute_complete_name', recursive=True,
        store=True)
    parent_id = fields.Many2one('godo.material.fertilizer.category', 'Nhóm cha', index=True, ondelete='cascade')
    parent_path = fields.Char(index=True)
    child_id = fields.One2many('godo.material.fertilizer.category', 'parent_id', 'Nhóm con')
    # production_item_count = fields.Integer(
    #     '# Products', compute='_compute_production_count',
    #     help="The number of production items under this category (Does not consider the children categories)")

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = '%s/%s' % (category.parent_id.complete_name, category.name)
            else:
                category.complete_name = category.name

    # def _compute_production_count(self):
    #     read_group_res = self.env['godo.production.item'].read_group([('categ_id', 'child_of', self.ids)], ['categ_id'], ['categ_id'])
    #     group_data = dict((data['categ_id'][0], data['categ_id_count']) for data in read_group_res)
    #     for categ in self:
    #         product_count = 0
    #         for sub_categ_id in categ.search([('id', 'child_of', categ.ids)]).ids:
    #             product_count += group_data.get(sub_categ_id, 0)
    #         categ.product_count = product_count

    @api.constrains('parent_id')
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive categories.'))

    @api.model
    def name_create(self, name):
        return self.create({'name': name}).name_get()[0]

    def name_get(self):
        if not self.env.context.get('hierarchical_naming', True):
            return [(record.id, record.name) for record in self]
        return super().name_get()

    # @api.ondelete(at_uninstall=False)
    # def _unlink_except_default_category(self):
    #     main_category = self.env.ref('g_production.production_item_category_root')
    #     if main_category in self:
    #         raise UserError(_("You cannot delete this product category, it is the default generic category."))

class GodoMaterialFertilizer(models.Model):
    _name = 'godo.material.fertilizer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Phân bón'      
    _order = 'name'

    name = fields.Char('Tên phân bón')
    image = fields.Image('Hình ảnh')
    package = fields.Char('Đóng gói')
    net_weight = fields.Float('Khối lượng tịnh (kg)')
    registered_owner = fields.Char('Tổ chức/cá nhân đăng ký')
    fertilizer_type = fields.Many2one(comodel_name='godo.material.fertilizer.category', string='Nhóm phân bón')
    composition_fertilizer_rate = fields.Char('Thành phần (%)')
    composition_fertilizer_ppm = fields.Char('Thành phần (ppm)')
    ph_value = fields.Char('Độ PH')
    proportion_value = fields.Char('Tỷ trọng')
    description = fields.Text('Mô tả')
    state = fields.Selection(selection=[('draft','Nháp'),('activated','Đang sử dụng'),('inactivated','Đã hủy')],   index=True, tracking=3, default='activated')

class GodoMaterialPesticidesCategory(models.Model):
    _name = 'godo.material.pesticides.category'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Pesticides Category'   
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = 'complete_name'
    _order = 'complete_name'

    name = fields.Char('Tên nhóm', index=True, required=True)
    complete_name = fields.Char(
        'Tên nhóm', compute='_compute_complete_name', recursive=True,
        store=True)
    parent_id = fields.Many2one('godo.material.pesticides.category', 'Nhóm cha', index=True, ondelete='cascade')
    parent_path = fields.Char(index=True)
    child_id = fields.One2many('godo.material.pesticides.category', 'parent_id', 'Nhóm con')
    # production_item_count = fields.Integer(
    #     '# Products', compute='_compute_production_count',
    #     help="The number of production items under this category (Does not consider the children categories)")

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = '%s/%s' % (category.parent_id.complete_name, category.name)
            else:
                category.complete_name = category.name

    # def _compute_production_count(self):
    #     read_group_res = self.env['godo.production.item'].read_group([('categ_id', 'child_of', self.ids)], ['categ_id'], ['categ_id'])
    #     group_data = dict((data['categ_id'][0], data['categ_id_count']) for data in read_group_res)
    #     for categ in self:
    #         product_count = 0
    #         for sub_categ_id in categ.search([('id', 'child_of', categ.ids)]).ids:
    #             product_count += group_data.get(sub_categ_id, 0)
    #         categ.product_count = product_count

    @api.constrains('parent_id')
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive categories.'))

    @api.model
    def name_create(self, name):
        return self.create({'name': name}).name_get()[0]

    def name_get(self):
        if not self.env.context.get('hierarchical_naming', True):
            return [(record.id, record.name) for record in self]
        return super().name_get()

    # @api.ondelete(at_uninstall=False)
    # def _unlink_except_default_category(self):
    #     main_category = self.env.ref('g_production.production_item_category_root')
    #     if main_category in self:
    #         raise UserError(_("You cannot delete this product category, it is the default generic category."))
 