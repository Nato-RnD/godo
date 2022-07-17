from odoo import models, fields, api,_


class ResPartner(models.Model):
    _inherit ='res.partner'
    _description = _('Partner')

    _customer_ranking = [
       ( 'rank_a', 'Rank A'),
       ( 'rank_b', 'Rank B'),
       ( 'rank_c','Rank C'),
       ( 'rank_d', 'Rank D'),
       ( 'rank_e','Rank E')
    ]

    province_id = fields.Many2one(comodel_name='res.province',string='Province')
    district_id = fields.Many2one(comodel_name='res.district', string='District')
    ward_id = fields.Many2one(comodel_name='res.ward',string='Ward')
    customer_rank = fields.Selection(string='Customer Rank', selection=_customer_ranking, default='rank_e')


    @api.onchange('province_id')
    def province_onchange(self):
        res = {}
        self.district_id = False
        parent_code = ''
        if self.province_id:
            list_district = self.env['res.district'].search([('parent_code', '=', self.province_id.province_code)])
            if len(list_district) > 0:
                parent_code = list_district[1].parent_code
            res = {'domain': {'district_id': [('parent_code', '=', parent_code)]}}
        else:
            res = {}
        return res    

    @api.onchange('district_id')
    def district_onchange(self):
        res = {}
        self.ward_id = False
        parent_code = ''
        if self.district_id:
            list_ward = self.env['res.ward'].search([('parent_code', '=', self.district_id.district_code)])
            if len(list_ward) > 0:
                parent_code = list_ward[0].parent_code
            res = {'domain': {'ward_id': [('parent_code', '=', parent_code)]}}
        return res
