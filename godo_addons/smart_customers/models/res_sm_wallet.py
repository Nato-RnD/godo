from locale import currency
import string
from odoo import models, fields, api,_

class ResSmWallet(models.Model): 
    _name = 'res.sm.wallet'
    _description = _('Wallet')
    
    _sql_constraints = [('account','UNIQUE(account)',_("Account Code must unique!")),('wallet_code','UNIQUE(wallet_code)',_("Wallet Code must unique!")),]

    account_id = fields.Many2one('res.account', string="Smart ID")
    wallet_code =   fields.Char(
        string='Wallet Code', 
    ) 
    name = fields.Char(string="Wallet name")
    currency_id =   fields.Many2one(
        string='Currency',
        comodel_name='res.currency',
        ondelete='restrict',
    )
    balance =  fields.Integer(
        string='Balance', compute='_get_balance', store = True
    )
    
    transaction_ids = fields.One2many(
        string='transaction',
        comodel_name='res.sm.transaction',
        inverse_name='wallet_id',
    )
    
    description = fields.Text(
        string='description',
    )
    status =   fields.Boolean(
        string='Status',
    ) 
    
    
    @api.onchange('account_id')
    def _get_account_id(self):
        self.wallet_code = 'W%s-%s' % (self.account_id.profile_code or '-', self.currency_id.name or '-')
        self.name = '%s %s %s' % (  self.currency_id.name,   _('wallets of'), self.account_id.profile_code  )
        
    @api.onchange('currency_id')
    def _get_currency_id(self):
        self.wallet_code = 'W%s-%s' % (self.account_id.profile_code or '-', self.currency_id.name or '-')
        self.name = '%s %s %s' % (  self.currency_id.name or '',   _('wallets of'), self.account_id.profile_code or ''  )
        
     
     
    
    @api.depends('transaction_ids.balance')
    def _get_balance(self):
        for record in self:
            comm_total = 0.0       
            for line in record.transaction_ids:      
                comm_total += line.balance    
            record.balance = comm_total
        
    
    
    
class ResSmTransaction(models.Model):
    _name ='res.sm.transaction'
    _description =  _('Transaction')
    
    name = fields.Char('Reference documents')
    account_id = fields.Many2one('res.account', string="Smart ID")
    wallet_id = fields.Many2one(
        string='Wallet',
        comodel_name='res.sm.wallet',
        ondelete='restrict',
    )
    in_amount =   fields.Integer(
        string='In amount',
    )
    out_amount = fields.Integer(
        string='Out amount',
    ) 
    balance = fields.Integer(
        string='Balance',
        compute = '_get_balance',
        store=True
    )

    description = fields.Text(string='Description')
    
    
    @api.depends('in_amount', 'out_amount')
    def _get_balance(self):
        for record in self:
            if record.in_amount > 0:
                record.balance = record.in_amount
            if record.out_amount > 0:
                record.balance = record.out_amount * -1
                
    @api.onchange('account_id')
    def account_id_onchange(self):
        profile_code_id= ''
        if self.account_id: 
            list_wallets = self.env['res.sm.wallet'].search([('account_id', '=', self.account_id.id)])
            if len(list_wallets) > 0:
                profile_code_id = list_wallets[0].account_id.id
            res = {'domain': {'wallet_id': [('account_id', '=', profile_code_id)]}}
            return res 
 
    
    @api.onchange('wallet_id')
    def wallet_id_onchange(self):
        if self.wallet_id:
            self.account_id = self.wallet_id.account_id.id
    
    
    
    
    
    
    
    
    