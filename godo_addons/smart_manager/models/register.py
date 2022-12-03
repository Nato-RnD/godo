# -*- coding: utf-8 -*-

from ast import Raise
from email.policy import default
from six import print_
from odoo import models, fields, api, _,registry, SUPERUSER_ID 
from odoo.models import check_method_name
from odoo.http import request
from odoo.service import db
import uuid
import base64
import json
import requests
import threading
import asyncio
import os 

from odoo.exceptions import UserError 
from odoo.api import call_kw, Environment 

from datetime import datetime
from dateutil.relativedelta import relativedelta
from time import sleep 

import logging
_logger = logging.getLogger(__name__)
_logger.debug("This is my debug message ! ")


class Register (models.Model):
    _name = 'smart_manager.register'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = _('Register Request')

    BUSINESS_TYPE_SELECTION =  [('person', 'Personal'), ('company', 'Company')]
    BUSINESS_SIZE_SELECTION = [( 0, '<10'), (1, '10-30'), (2, '31-50'), (3, '51-100'), (4, '100-200'), (5, '>200')]
    STATE_SELECTION = [( 'draft',_('Draft')),( 'registered',_('Registered')), ('verifying', _('Verifying')), ('verified', _('Verified')),
    ('initialing',_('Initialing')), ('activated', _('Activated')), ('expired', _('Expired')), ('cancelled', _('Cancelled'))]
    VERIFY_TYPE_SELECTION = [('mobile','Mobile'),('email','Email')]

    REGISTER_TYPE_SELECTION = [('monthly', _('Monthly')),('annualy',_('Annualy'))]
    REGISTER_QUANTITY_SELECTION = [(1,'1 month'),(3,'3 months'),(6,'6 months'),(9 ,'9 months')]
    USING_TYPE_SELECTION = [('trial', _('Trial')), ('business',_('On Business'))]

    #Business infomations  
    use_type =    fields.Selection(
        string='Using Type',
        selection=USING_TYPE_SELECTION
    )

    business_type =  fields.Selection(
        string='Business Type',
        selection=BUSINESS_TYPE_SELECTION
    )

    business_size =   fields.Selection(
        string='Business Size',
        selection=BUSINESS_SIZE_SELECTION
    ) 
    
    business_category =   fields.Many2one(
        string='Business Model',
        comodel_name='smart_manager.business_category',
        ondelete='restrict',
    )

    verify_type = fields.Selection(
        string='Verify Type',
        selection=VERIFY_TYPE_SELECTION,
        default="mobile"
    )

    state =   fields.Selection(
        string='Status',
        selection= STATE_SELECTION,
        default="draft"
    )
    note = fields.Text(string='Note')
     

    #Account infomation
    name = fields.Char(string='Shop Name')
    code = fields.Char(string='Register Code')
    business_tax_code = fields.Char(string='Tax Code')
    business_tax_address = fields.Char(string='Company tax address', none= True, blank=True) 
    shop_domain = fields.Char(string='Shop domain')
    partner = fields.Many2one(string='Partner', comodel_name='res.partner')
    
    

    order =    fields.One2many(
        string='Order',
        comodel_name='sale.order',
        inverse_name='order_register',
    )
   
    partner_name = fields.Char(string='Customer Name')
    mobile = fields.Char(string='Mobile')
    email = fields.Char(string='Email')

    register_date =   fields.Datetime(
        string='Register Date',
        default=fields.Datetime.now,
    )
    activated_date =  fields.Datetime(
        string='Activated Date',
    ) 
    expired_date = fields.Datetime(
        string='Expired Date',
    ) 

    register_type =   fields.Selection(
        string='Register Type',
        selection=REGISTER_TYPE_SELECTION,
        blank=False, none=False,
        required = True,
        default='monthly'
    )

    register_quantity = fields.Many2one(
        string='Register Quantity',
        comodel_name='smart_manager.payment_period',
        ondelete='restrict',
           required = True
    ) 
    province =  fields.Many2one(
        string='Province',
        comodel_name='res.province',
        ondelete='restrict',
    )
    district =  fields.Many2one(
        string='District',
        comodel_name='res.district',
        ondelete='restrict',
    )
    ward =  fields.Many2one(
        string='Ward',
        comodel_name='res.ward',
        ondelete='restrict',
    )
    
    admin_use =   fields.Boolean(
        string='Sử dụng Admin',
        default = True
    )
    

    username = fields.Char(string='Username')
    password = fields.Char(string='Password')
    database_uuid = fields.Char(string='Mã cơ sở dữ liệu')

    install_apps =   fields.Many2many(
        string='Install Apps',
        comodel_name='smart_manager.app_price',
        relation='smart_manager_register_app_price_rel',
        column1='register_id',
        column2='price_id',
        domain="[('enable', '=', True )]"
    ) 
 
    @api.onchange('register_type')
    def _onchange_register_type(self):
        _annualy_type =True if self.register_type == 'annualy' else False
        self.register_quantity = False
        self.install_apps = False
        return {'domain': {'register_quantity': [('is_annualy', '=',_annualy_type)]}}

    @api.onchange('register_quantity')
    def _onchange_register_quantity(self) :
        return {'domain': {'install_apps':[('period','=', self.register_quantity.id)]}}
    
    

    @api.onchange('province')
    def onchange_province(self):
        res = {}
        self.district = False
        parent_code = ''
        if self.province:
            list_district = self.env['district'].search([('parent_code', '=', self.province.code_province)])
            if len(list_district) > 0:
                parent_code = list_district[1].parent_code
            res = {'domain': {'district': [('parent_code', '=', parent_code)]}}
        else:
            res = {}
        return res    
 
    @api.onchange('district')
    def onchange_district(self):
        res = {}
        self.ward = False
        parent_code = ''
        if self.district:
            list_ward = self.env['ward'].search([('parent_code', '=', self.district.code_district)])
            if len(list_ward) > 0:
                parent_code = list_ward[0].parent_code
            res = {'domain': {'ward': [('parent_code', '=', parent_code)]}}
        return res

   
    @api.model
    def create(self, vals):  
            vals['password'] = self.encrypt(vals['password'])
            res = super().create(vals)  
            _code =  uuid.uuid4().hex
            res.code = _code.upper()
            return res

    @api.onchange('install_apps')
    def onchange_install_apps(self):
        list_app = self.install_apps.ids
        for e in self.install_apps:
            if e.app.depend_apps:
                for v in e.app.depend_apps:
                    app = self.env['smart_manager.app_price'].search([('period','=', self.register_quantity.id),('app','=',v.id)])
                    if app: 
                        list_app.append(app.id)
        self.update({'install_apps': [(6,0,list_app)] })
    

    # Action method  
    def action_register_register(self):
        if(db.exp_db_exist(self.shop_domain)==True): 
            raise UserError(_('Tên miền %s.smarterp.vn đã tồn tại, vui lòng thay đổi tên miền của shop!' % self.shop_domain))
        else:
            self.state = 'registered'
            msg = _('Biểu mẫu đăng ký %s đã được ghi nhận!' % self.code)
            self.message_post(body=msg)

    def action_register_verify(self):
        old_list_app = self.install_apps.ids
        new_list_app = []
        for e in self.install_apps:
            if e.app.depend_apps:
                for v in e.app.depend_apps:
                    app = self.env['smart_manager.app_price'].search([('period','=', self.register_quantity.id),('app','=',v.id)])
                    if app: 
                        new_list_app.append(app.id)
        if all(v in old_list_app for v in new_list_app):
            self.state = 'verifying' 
            msg = _('The request form %s is verifying now!' % self.code)
            self.message_post(body=msg)
        else:
            error = 'Không đủ app kèm theo'
            return UserError(_(error)) 

    def action_register_confirm(self):  
        vals = {
                'name': self.partner_name,
                'vat': self.business_tax_code or None,
                'mobile': self.mobile or None, 
                'company_type': self.business_type or None,
                'email': self.email or None,
                'province':self.province.id or '',
                'district':self.district.id or '',
                'ward':self.ward.id or '',
            }
        self.partner = self.env['res.partner'].sudo().create(vals) 
        self.state = 'verified'
        msg = _('Biểu mẫu đăng ký %s đã được xác thực!' % self.code)
        self.message_post(body=msg)
  
    def action_register_re_verify(self):
        self.state = 'verifying'


    def action_register_cancel(self): 
        self.state = 'cancelled'
        msg = _('Biểu mẫu đăng ký %s đã bị hủy bỏ!' % self.code)
        self.message_post(body=msg)

    def action_register_to_draft(self):
        self.state = 'draft' 
        msg = _('Đã chuyển biểu mẫu %s về trạng thái nháp!' % self.code)
        self.message_post(body=msg)
        
    def action_register_close_service(self):
        self.state = 'expired' 
        self._set_expired(self.shop_domain)
        msg = _('Dịch vụ đăng ký %s đã hết hạn!' % self.code)
        self.message_post(body=msg)   
        
    def action_regster_re_active(self):
        if self.expired_date < datetime.now():
            raise UserError(_('Thời gian hết hạn phải lớn hơn hiện tại, vui lòng chọn sửa biểu mẫu và gia hạn dịch vụ!'))
        
        self.state = 'activated' 
        self._set_activate(self.shop_domain)
        msg = _('Dịch vụ %s đã được kích hoạt lại!' % self.code)
        self.message_post(body=msg)       
         
         
    def action_regster_re_bill(self):
        if self.expired_date < datetime.now():
            raise UserError(_('Thời gian hết hạn phải lớn hơn hiện tại, vui lòng chọn sửa biểu mẫu và gia hạn lại!'))  
        self.state = 'activated' 
        _order = self.env['sale.order'].create({
                    'partner_id': self.partner.id,
                    'state':'draft',
                    'order_line': [(0, 0, {
                        'name': (product.app.name if product.app.default_code == False else '[%s] %s'%(product.app.default_code,product.app.name) ), 
                        'product_id': product.app.id, 
                        'product_uom_qty': 1, 
                        'product_uom': product.app.uom_id.id, 
                        'price_unit': product.price}) for product in self.install_apps],
                    'app_sale':True,
                    'order_register':self.id,
                })
        create_invoice_config = bool(self.env['ir.config_parameter'].sudo().get_param('smart_manager.create_invoice'))
        if self.use_type == 'business' and create_invoice_config : 
            Invoice = self.env['account.invoice']
            _order.order_line.read(['name', 'price_unit', 'product_uom_qty', 'price_total']) 
            _order.force_quotation_send()
            _order.order_line._compute_product_updatable() 

            _order.action_confirm() 
            inv_id = _order.action_invoice_create()
            Invoice.browse(inv_id)
            _order.order_line._compute_product_updatable()
               
        order = _order
        self.ensure_one() 
        update_order = [(6, 0, [order.id])]
        self.write({ 'order':update_order })      
        self._set_activate(self.shop_domain)
    
        
    def action_register_active_admin(self):
        if self.admin_use:
            raise UserError('User Admin đã được kích hoạt!')
        
        try: 
            with registry(self.shop_domain).cursor() as new_cr:
                env = api.Environment(new_cr, SUPERUSER_ID, {})
                Iuser = env['res.users'] 
                admin = Iuser.with_context(
    active_test=False).search([('login','=','admin@smarterp.vn')])
                if admin:
                    admin.active = True
                # return True
            self.admin_use = True
        except Exception as e:
            return False
        
    def action_register_deactive_admin(self):
        if not self.admin_use:
            raise UserError('User Admin đã được hủy kích hoạt!')
        
        try: 
            with registry(self.shop_domain).cursor() as new_cr:
                env = api.Environment(new_cr, SUPERUSER_ID, {})
                Iuser = env['res.users'] 
                admin = Iuser.with_context(
    active_test=False).search([('login','=','admin@smarterp.vn')])
                if admin:
                    admin.active = False
                # return True
            self.admin_use = False
        except Exception as e:
            return False
    def _call_kw(self, model, method, args, kwargs):
        check_method_name(method)
        return call_kw(request.env[model], method, args, kwargs)

    def action_register_create_database(self) : 
        with api.Environment.manage():  
            new_cr = self.pool.cursor()
            this = self.with_env(self.env(cr=new_cr))  
            try:
                
                list_apps = [i.app.default_code for i in this.install_apps]  
                
                user_admin_config = this.env['ir.config_parameter'].sudo().get_param('smart_manager.user_admin'),
                if user_admin_config[0]:
                    _super_users = user_admin_config[0]
                    _passw_super_users = '%s123..' % user_admin_config[0].split('@')[0]
                else:
                    _super_users = 'admin@smarterp.vn'
                    _passw_super_users = 'admin123..'
                     
                _logger.info('Start create database')   
                this._exp_create_database(this.shop_domain, False, 'vi_VN', _passw_super_users, _super_users, 'vn', this.partner.mobile)  
                
                this._register_database_uuid()
                
                _logger.info('Database Created')  
                #Create new user after create db complete
                _logger.info('Start create user')
                this._register_new_user(this.shop_domain,this.partner_name, this.username, this.decrypt(this.password ))
                _logger.info('User created')
               
                _logger.info('Start install apps')
                this._register_install_app(this.shop_domain,list_apps)  
                _logger.info('Apps installed')
                
                _logger.info('Set activated for customer')
                
                _exp =  fields.Datetime.to_datetime(datetime.now() + relativedelta(months=this.register_quantity.value)) if(this.register_type == 'monthly') else fields.Datetime.to_datetime(datetime.now() + relativedelta(years=this.register_quantity.value))
                
                with registry(new_cr.dbname).cursor() as new_cr:
                    env = api.Environment(new_cr, SUPERUSER_ID, {})
                    _register = env['smart_manager.register'].search([('id','=',this.id)])[0] 
                    _register.state = 'activated'
                    _register.activated_date = fields.Datetime.to_datetime(datetime.now()) 
                    _register.expired_date =_exp
                      
                
                return 
            except Exception as e:
                _logger.error('Error client')
                _logger.error(str(e))
                self.state = 'verified'
                self._cr.commit()
                self._cr.rollback()
                self._cr.close()
                error = "Database creation error: %s" % self.shop_domain 
                return UserError(_(error)) 
    
    def action_register_init_db(self): 
        try:
            self.write({ 'state':'initialing' }) 
            # create sale order if db not exist
            if  not db.exp_db_exist(self.shop_domain): 
                _order = self.env['sale.order'].create({
                    'partner_id': self.partner.id,
                    'state':'draft',
                    'order_line': [(0, 0, {
                        'name': (product.app.name if product.app.default_code == False else '[%s] %s'%(product.app.default_code,product.app.name) ), 
                        'product_id': product.app.id, 
                        'product_uom_qty': 1, 
                        'product_uom': product.app.uom_id.id, 
                        'price_unit': product.price}) for product in self.install_apps],
                    'app_sale':True,
                    'order_register':self.id,
                }) 
                
                create_invoice_config = bool(self.env['ir.config_parameter'].sudo().get_param('smart_manager.create_invoice'))
                if self.use_type == 'business' and create_invoice_config : 
                    Invoice = self.env['account.invoice']
                    _order.order_line.read(['name', 'price_unit', 'product_uom_qty', 'price_total']) 
                    _order.force_quotation_send()
                    _order.order_line._compute_product_updatable() 

                    _order.action_confirm() 
                    inv_id = _order.action_invoice_create()
                    Invoice.browse(inv_id)
                    _order.order_line._compute_product_updatable()
               
                order = _order
                self.ensure_one()
                
                update_order = [(6, 0, [order.id])]
                self.write({ 'order':update_order })  
           
            else:
                raise UserError(_('Tên miền %s.smarterp.vn đã tồn tại, vui lòng thay đổi tên miền của shop!' % self.shop_domain))    
            
        except Exception as e:
            self.state = 'verified'

        _logger.info('Update state')
        
        # asyncio.create_task(self.action_register_create_database) 
        threaded_calculation = threading.Thread(target=self.action_register_create_database ) 
        threaded_calculation.setDaemon(True)
        threaded_calculation.start() 
        return True 

    def encrypt(self, char):
        _pwd = base64.b64encode(str.encode(char)).hex()
        return _pwd


    def decrypt(self,key):
        _char = base64.b64decode(bytes.fromhex(key))
        return _char.decode("ascii")

    def get_traffic(self): 
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        list_url = base_url.split('://')
        url = list_url[0]+"://"+self.shop_domain+"*"
 
        return self.env['report.traffic'].reload_data({'url':url})
    
    
    @db.check_db_management_enabled
    def _exp_create_database(self,db_name, demo, lang, user_password, login, country_code=None, phone=None): 
        try:
            _logger.info('Create database `%s`.', db_name)
            db._create_empty_database(db_name)
            db._initialize_db(id, db_name, demo, lang, user_password, login, country_code, phone)
            return True
        except Exception as e:
            return False

    @api.model
    def _register_new_user(self,db,name, username, password):
        try: 
            with registry(db).cursor() as new_cr:
                env = api.Environment(new_cr, SUPERUSER_ID, {})
                Iuser = env['res.users']
                user = Iuser.create({'name':name,'login': username,'password': password}) 
                _access_rights = env.ref('base.group_erp_manager')
                _technical_feature = env.ref('base.group_no_one')
                _internal_user = env.ref('base.group_user')
                _contact_creation = env.ref('base.group_partner_manager') 
                _system = env.ref('base.group_system')
                for item in (_system,_access_rights,_technical_feature,_internal_user,_contact_creation) :
                    item.write( {'users':[(4, user.id)] 
                        }) 
                    
                admin = Iuser.search([('login','=','admin@smarterp.vn')])
                if admin:
                    admin.active = False
                return True
        except Exception as e:
            return False
        
    @api.model
    def _register_database_uuid(self):
        try: 
            uuid = self._get_database_uuid(self.shop_domain)
            new_cr = self.pool.cursor()
            with registry(new_cr.dbname).cursor() as new_cr:
                    env = api.Environment(new_cr, SUPERUSER_ID, {})
                    _register = env['smart_manager.register'].search([('id','=',self.id)])[0] 
                    _register.database_uuid = uuid 
        except Exception as e:
            return False
        
        
    @api.model
    def _get_database_uuid(self,db):
        try: 
            with registry(db).cursor() as new_cr:
                env = api.Environment(new_cr, SUPERUSER_ID, {})
                get_param = env['ir.config_parameter'].sudo()
                set_param = env['ir.config_parameter'].sudo().set_param
                
                set_param('database.expiration_date', self.expired_date) 
                set_param('database.enterprise_code', self.code)  
                
                return get_param.get_param('database.uuid',False) 
        except Exception as e:
            return False
        
            
    @api.model
    def _register_install_app(self,db,app_codes): 
        try:
            with registry(db).cursor() as new_cr:
                env = api.Environment(new_cr, SUPERUSER_ID, {}) 
                IrModule = env['ir.module.module']
                    
                modules = IrModule.search([('name','in', app_codes) ])
                if len(modules) >0: 
                    modules.button_immediate_install()  
            return True
        except Exception as e:
            return False
    

    @api.model
    def _set_expired(self,db):
        try: 
            with registry(db).cursor() as new_cr:
                env = api.Environment(new_cr, SUPERUSER_ID, {})
                set_param = env['ir.config_parameter'].sudo().set_param
                set_param('database.expiration_date', datetime.now())
                set_param('database.expiration_reason','Nhà cung cấp đã cắt dịch vụ')
                # set_param('database.enterprise_code', self.code)  
                return True
        except Exception as e:
            return False
        
    @api.model
    def _set_activate(self,db):
        try: 
            with registry(db).cursor() as new_cr:
                env = api.Environment(new_cr, SUPERUSER_ID, {})
                set_param = env['ir.config_parameter'].sudo().set_param
                set_param('database.expiration_date', self.expired_date)
                set_param('database.expiration_reason',False) 
                return True
        except Exception as e:
            return False