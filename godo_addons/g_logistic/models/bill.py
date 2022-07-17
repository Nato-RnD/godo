from email.policy import default
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


class LogisticBillInventory(models.Model):
    _name = 'godo.logistic.bill.inventory'
    _inherit =['mail.thread', 'mail.activity.mixin'] 
    _description = 'Bill Inventory'

    _inventory_selection = [
       ( 'draft', 'Draft'),
       ( 'done', 'Done'), 
       ( 'cancelled','Cancelled')
    ]

    name = fields.Char(string='Inventory Check', required=True)
    date = fields.Date(string='Date', required=True)
    user_id = fields.Many2one(comodel_name= 'res.users', string='Employee ID')
    bill_ids = fields.Many2many(comodel_name='godo.logistic.bill', relation='godo_logistic_bill_inventory_rel', string='Bills')
    note =fields.Text('Note')
    state = fields.Selection(string='Status', selection=_inventory_selection, default='draft')
    search = fields.Char(string='Search', default='')


    @api.onchange('search')
    def _bill_search(self):
        pass
        # if self.search != '' and self.search is not None:
        #     _bill_id = self.env['godo.logistic.bill'].search(['|',('name','like',self.search),('origin_code','like',self.search)],limit=1)
        #     if _bill_id:
        #         self.bill_ids.append(_bill_id)

 