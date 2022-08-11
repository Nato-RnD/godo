from datetime import datetime
from unicodedata import name
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
    
    _bill_status = [( 'received', 'Received'),
       ( 'forward','Forwarded'),
       ( 'done', 'Done'),
       ( 'cancelled','Cancelled')]

    name = fields.Char(string='Bill Check', required=True)
    date = fields.Date(string='Date', default=fields.Date.today())
    user_id = fields.Many2one(comodel_name= 'res.users', string='Employee ID', default=lambda self: self.env.user and self.env.user.id or False)
    bill_ids = fields.Many2many(comodel_name='godo.logistic.bill', relation='godo_logistic_bill_check_rel',  column1='check_id', column2='bill_id_rec', string='Bills')
    bill_count = fields.Integer(string='Bill count')
    note =fields.Text(string='Note')
    state = fields.Selection(string='Status', selection=_check_selection, default='draft')
    search_text = fields.Char(string='Search', default='')
    check_type = fields.Selection(selection=_bill_status,string='Check Type')
    

 
    @api.onchange('search_text')
    def _bill_search(self): 
        if self.search_text != '' and self.search_text is not None:
            _bill_id = self.env['godo.logistic.bill'].sudo().search(['|',('name','like',self.search_text),('origin_code','like',self.search_text)],limit=1)
            if _bill_id:
                self.bill_ids =[(4,_bill_id.id)]
                self.bill_count = len(self.bill_ids)
                
        return {}


 
    def bill_check_confirm(self):
        self.ensure_one()
        if self.check_type is not None:
            for bill in self.bill_ids:
                bill.state = self.check_type
                if self.check_type == 'done':
                    bill.done_date = datetime.now()
            self.state = 'done'
            self.message_post(body= _('%s confirmed the bill check %s' % (self.user_id.name, self.name) ))
                
        
    
 
    def bill_check_cancel(self):
        self.ensure_one()
        if self.id is not None:
            self.state='cancelled'
            self.message_post(body= _('%s cancelled the bill check %s' % (self.user_id.name, self.name) ))