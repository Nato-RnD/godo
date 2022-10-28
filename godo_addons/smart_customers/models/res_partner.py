from odoo import models, fields, api,_

class ResPartner(models.Model): 
    _inherit = 'res.partner'
    
    
    _sql_constraints = [('profile_code','UNIQUE(profile_code)',_("Profile Code must unique!")),]

    account = fields.Many2one('res.account', string="Smart ID")
    profile_code = fields.Char(string="Smart ID")
    province = fields.Many2one(comodel_name='res.province', string='Province')
    district = fields.Many2one(comodel_name='res.district',string='District')
    ward = fields.Many2one(comodel_name='res.ward', string='Ward')
    is_service_customer = fields.Boolean(default=False)
    wallet_ids =  fields.One2many(
        string='Wallets',
        comodel_name='res.sm.wallet',
        inverse_name='account_id',
    )
    
    
    
    @api.onchange('province')
    def onchange_province(self):
        res = {}
        self.district = False
        parent_code = ''
        if self.province:
            list_district = self.env['res.district'].search([('parent_code', '=', self.province.province_code)])
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
            list_ward = self.env['res.ward'].search([('parent_code', '=', self.district.district_code)])
            if len(list_ward) > 0:
                parent_code = list_ward[0].parent_code
            res = {'domain': {'ward': [('parent_code', '=', parent_code)]}}
        return res
    
    @api.onchange('account')
    def onchange_account(self):
        self.profile_code = self.account.profile_code
        self.is_service_customer =True
        


 