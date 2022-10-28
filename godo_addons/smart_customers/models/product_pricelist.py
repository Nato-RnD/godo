from locale import currency
import string
from odoo import models, fields, api,_

class ProductPricelist(models.Model): 
    _inherit = 'product.pricelist'
    _description = _('Price list')
    
    only_service_pricelist = fields.Boolean(
        string='Service Only',
    ) 
    in_use =   fields.Boolean(
        string='In Use',
    )
    affiliate_award_point =   fields.Integer(
        string='Affiliate award points',
    )
     
    
class ProductPricelistItem(models.Model): 
    _inherit = 'product.pricelist.item'
    _description = _('Price list Item')
    
    auto_verify =   fields.Boolean(
        string='Auto Verify',
    )
    
    award_point =   fields.Integer(
        string='Award points',
    )
    
    
    
    
    
    
    
    