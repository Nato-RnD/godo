#-*- coding: utf-8 -*-

from soupsieve import select
from odoo import SUPERUSER_ID, models, fields, api, tools
from odoo.exceptions import UserError, ValidationError

class GodoProductionItemCategory(models.Model):
    _name = 'godo.production.item.category'
    _description = 'Production Item Category'
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = 'complete_name'
    _order = 'complete_name'

    name = fields.Char('Tên nhóm', index=True, required=True)
    complete_name = fields.Char(
        'Tên nhóm', compute='_compute_complete_name', recursive=True,
        store=True)
    parent_id = fields.Many2one('godo.production.item.category', 'Nhóm cha', index=True, ondelete='cascade')
    parent_path = fields.Char(index=True)
    child_id = fields.One2many('godo.production.item.category', 'parent_id', 'Nhóm con')
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

    @api.ondelete(at_uninstall=False)
    def _unlink_except_default_category(self):
        main_category = self.env.ref('g_production.production_item_category_root')
        if main_category in self:
            raise UserError(_("You cannot delete this product category, it is the default generic category."))
 
 
class GodoProductionItem(models.Model):
    _name = 'godo.production.item'
    _description = 'Production Item'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'code, name, id desc' 

    @tools.ormcache()
    def _get_default_category_id(self):
        # Deletion forbidden (at least through unlink)
        return self.env.ref('g_production.production_item_category_root')

    def _read_group_categ_id(self, categories, domain, order):
        category_ids = self.env.context.get('default_categ_id')
        if not category_ids and self.env.context.get('group_expand'):
            category_ids = categories._search([], order=order, access_rights_uid=SUPERUSER_ID)
        return categories.browse(category_ids)
        
    
    name = fields.Char('Item name', required=True)
    code = fields.Char('Item code')
    image = fields.Image('Ảnh')
    categ_id = fields.Many2one(
        'godo.production.item.category', 'Product Category',
        change_default=True, default=_get_default_category_id, group_expand='_read_group_categ_id',
        required=True, help="Select category for the current product")
    state = fields.Selection(selection=[('draft','Nháp'),('done','Đang sử dụng'),('cancelled','Đã hủy')],   index=True, tracking=3, default='draft')

    # partner_ref = fields.Char('Customer Ref', compute='_compute_partner_ref')



class GodoProductionSeed(models.Model):
    _name = 'godo.production.seed'
    _description = 'Production Seed'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'code, name, id desc' 

    @tools.ormcache()
    def _get_default_category_id(self):
        # Deletion forbidden (at least through unlink)
        return self.env.ref('g_production.production_item_category_root')

    def _read_group_categ_id(self, categories, domain, order):
        category_ids = self.env.context.get('default_categ_id')
        if not category_ids and self.env.context.get('group_expand'):
            category_ids = categories._search([], order=order, access_rights_uid=SUPERUSER_ID)
        return categories.browse(category_ids)


    name = fields.Char('Tên giống', required=True)
    code = fields.Char('Mã giống')
    location = fields.Char('Vùng được phép sản xuất')
    cert_num = fields.Char('Số thông tư, quy định công nhận')
    seed_num = fields.Char('Mã hàng')
    cert_date = fields.Date('Ngày tháng')
    categ_id = fields.Many2one(
        'godo.production.item.category', 'Loại giống',
        change_default=True, default=_get_default_category_id, group_expand='_read_group_categ_id',
        required=True, help="Select category for the current seed")
    image = fields.Image('Ảnh')
    
    state = fields.Selection(selection=[('draft','Nháp'),('done','Đang sử dụng')], string='Trạng thái',   index=True, tracking=2, default='done')


    def action_open_label_layout(self):
        action = self.env['ir.actions.act_window']._for_xml_id('product.action_open_label_layout')
        action['context'] = {'default_product_ids': self.ids}
        return action