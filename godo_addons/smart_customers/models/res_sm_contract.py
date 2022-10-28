from locale import currency
import string
from odoo import models, fields, api,_

class ResSmContract(models.Model):  
    _inherit = 'sale.order'
    _description = _('Contract')
     
    contract_code = fields.Char(
        string='Contract Number',default=lambda self: _('HD-DV/0000')
    )
     
    customer_tax_code =   fields.Char(
        string='Tax Code',
    )
    
    customer_address = fields.Char(string='Address')
     
 
    contract_mode = fields.Selection(
        string='Register Mode',
        selection=[('trial', 'Trial'), ('business', 'Business'),('testing','Testing')]
    )
    
    affiliated_account_id =  fields.Many2one(
        string='Affiliated Account',
        comodel_name='res.account',
        ondelete='restrict',
    ) 
    
    service_contract = fields.Boolean(
        string='Service Contract',
    )
    
    @api.onchange('partner_id')
    def partner_id_onchange(self):
        self.customer_tax_code = self.partner_id.vat
        address = [self.partner_id.street or '',self.partner_id.ward.name or '',self.partner_id.district.name or '',self.partner_id.province.name or '']
        address[:] = [add for add in address if add] 
        self.customer_address =  ', '.join(address)
        self.service_contract = True 
        
    @api.model
    def create(self, vals):
        if vals.get('contract_code', _('HD-DV/0000')) == _('HD-DV/0000'):
            seq_date = None
            if 'date_order' in vals:
                seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_order']))
            if 'company_id' in vals:
                vals['contract_code'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'contract.order', sequence_date=seq_date) or _('HD-DV/0000')
            else:
                vals['contract_code'] = self.env['ir.sequence'].next_by_code('contract.order', sequence_date=seq_date) or _('HD-DV/0000') 
                
        result = super(ResSmContract, self).create(vals)
        return result
class ResSmContractLine(models.Model): 
    _inherit = 'sale.order.line'
    _description = _('Contract Line')
    
     
    
    
    
    
        
    
    
    
    
    

    

    
    
    