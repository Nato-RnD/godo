from odoo import models, fields, api, _
from .services import contract_service_pb2_grpc, contract_service_pb2
from concurrent import futures
from .grpc_server import *
_logger = logging.getLogger(__name__)


class ResAccount(models.Model): 
    _name = 'res.account'
    _description = 'User Account'
    
    _sql_constraints = [('profile_code','UNIQUE(profile_code)',_("Profile Code must unique!")),]
    
    name = fields.Char(string='Name')
    acc_code = fields.Char(string="Acc Code")
    user_name = fields.Char(string="Username")
    profile_code = fields.Char(string="Profile Code")
    last_name = fields.Char(string="Last Name")
    first_name = fields.Char(string="first Name")
    date_of_birth = fields.Integer(string="Date of Birth")
    gender = fields.Char(string="Smart ID")
    email = fields.Char(string="Email")
    mobile = fields.Char(string="Mobile")
    avatar = fields.Char(string="Avatar")
    wall_background = fields.Char(string="Wall Background")
    email = fields.Char(string="Email")
    register_date = fields.Integer(string="Date of Register")
    province = fields.Many2one(comodel_name='res.province', string='Province')
    district = fields.Many2one(comodel_name='res.district',string='District')
    ward = fields.Many2one(comodel_name='res.ward', string='Ward')
    status = fields.Boolean(string='Status')
    
    
    
    # @api.depends('profile_code','last_name','first_name','user_name')
    # def _get_name(self):
    #     for record in self:
    #         record.name = '%s [%s %s - %s]' % (record.profile_code, record.last_name, record.first_name, record.user_name)
     

    # def name_get(self):
    #     res = []
    #     for record in self: 
    #         res.append((record.id, '%s [%s %s - %s]' % (record.profile_code, record.last_name, record.first_name, record.user_name)))
            
    #     return res
    
    

 


    def overview_dashboard(self,*options,**kws):
        ctx = {
            'html': '<h1>Thong bao</h1>',
            'header_html': '<h1>Thong bao</h1>', 
            'header_title': 'Tieu de tren nhe',
        } 
        return ctx


    