from odoo import models, fields, api,_ 

class LogisticBillCheck(models.Model):
    _name = 'godo.logistic.bill.check'
    _description =  _('Bill Check')
    _inherit =['mail.thread', 'mail.activity.mixin'] 


    _check_selection = [
       ( 'draft', 'Draft'),
       ( 'done', 'Done'), 
       ( 'cancelled','Cancelled')
    ]

    name = fields.Char(string='Bill Check', required=True)
    date = fields.Date(string='Date', default=fields.Date.today())
    user_id = fields.Many2one(comodel_name= 'res.users', string='Employee ID', default=lambda self: self.env.user and self.env.user.id or False)
    bill_ids = fields.Many2many(comodel_name='godo.logistic.bill',  column1='check_id', column2='bill_id', string='Bills')
    bill_count = fields.Integer(string='Bill count')
    note =fields.Text(string='Note')
    state = fields.Selection(string='Status', selection=_check_selection, default='draft')
    search_text = fields.Char(string='Search', default='')

 
    @api.onchange('search_text')
    def _bill_search(self): 
        if self.search_text != '' and self.search_text is not None:
            _bill_id = self.env['godo.logistic.bill'].sudo().search(['|',('name','like',self.search_text),('origin_code','like',self.search_text)],limit=1)
            if _bill_id:
                self.bill_ids =[(4,_bill_id.id)]
                self.bill_count = len(self.bill_ids)
                
        return {}
