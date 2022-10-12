from odoo import models, fields, api,_ 

class LogisticBill(models.Model):
   _name = 'godo.logistic.bill'
   _description = _('Logistic Bill')
   _inherit =['mail.thread', 'mail.activity.mixin'] 
   _bill_selection = [
       ( 'sent', 'Sent from China'),
       ( 'received', 'Received'),
       ( 'forward','Forwarded'),
       ( 'done', 'Done'),
       ( 'cancelled','Cancelled')
    ]

   name = fields.Char(string='Bill code')
   origin_code = fields.Char(string='Origin Code')
   packing_code = fields.Char('Packing code')
   bill_date = fields.Date(string='Bill date', default= fields.Date.today())
   done_date = fields.Datetime(string='Done date')
   customer_id = fields.Many2one(comodel_name='res.partner', string='Customer')
   customer_address = fields.Char(string='Address')
   customer_mobile = fields.Char('Mobile')
   goods_name = fields.Char('Goods name')
   package_weight = fields.Float(string='Weight')
   unit_price = fields.Float(string='Unit price')
   unit_quantity = fields.Integer(string='Quantity')
   total_amount = fields.Float(string='Total amount')
   note = fields.Text(string='Note')
   state = fields.Selection(string='Status', selection=_bill_selection, default='sent')
   bill_check_ids = fields.Many2many(comodel_name='godo.logistic.bill.check', relation='godo_logistic_bill_check_rel',  column1='bill_id_rec', column2='check_id', string='Bill Checks')
   
   @api.onchange('customer_id')
   def customer_id_onchange(self):
          if self.customer_id:
            self.customer_mobile = self.customer_id.mobile
            self.customer_address = '%s %s %s %s' % (self.customer_id.street or '', self.customer_id.ward_id.name or '', self.customer_id.district_id.name or '' , self.customer_id.province_id.name or '')

  