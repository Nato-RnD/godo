from locale import currency
import string
from odoo import models, fields, api,_

class ProductTemplate(models.Model): 
    _inherit = 'product.template'
    _description = _('Product')
    
    software_ok =   fields.Boolean(
        string='Is Software',
    )
    
    software_id =   fields.Many2one(
        string='App ID',
        comodel_name='res.apps',
        ondelete='restrict',
    )
    
    
    @api.onchange('software_id')
    def software_id_onchange (self):
        self.barcode = self.software_id.app_code
        self.default_code = self.software_id.app_code
        self.name =self.software_id.name
          
    
    
    