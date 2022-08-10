from odoo import http
from odoo.http import request
import random
class BillSearch(http.Controller):
   @http.route(['/bill-search'], type="json", auth="public")
   def bill_search(self, **kw):
        _bill_selection = [
       ( 'sent', 'Sent from China'),
       ( 'received', 'Received'),
       ( 'forward','Forwarded'),
       ( 'done', 'Done'),
       ( 'cancelled','Cancelled')
    ] 
        _color_selection =   [
       ( 'sent', 'alert alert-primary'),
       ( 'received', 'alert alert-info'),
       ( 'forward','alert alert-danger'),
       ( 'done', 'alert alert-success'),
       ( 'cancelled','alert alert-secondary')
    ]
        _icon_selection =   [
       ( 'sent', 'fa fa-send'),
       ( 'received', 'fa fa-calendar-check-o'),
       ( 'forward','fa fa-truck'),
       ( 'done', 'fa fa-map-signs'),
       ( 'cancelled','fa fa-lock')
    ]
        
        badge_color = ('bg-warning','bg-success','bg-danger','bg-info') 
        bill_code = kw.get('code',None)
        if bill_code is not None:
           bill = request.env['godo.logistic.bill'].sudo().search(['|',('origin_code','=',bill_code),('name','=',bill_code)],limit=1)
           if bill: 
                transfer_history = [{ 
                   'date': bill.bill_date,
                   'name': _bill_selection[0][1], 
                   'bgcolor': random.choice(badge_color),
                   'icon': _icon_selection[0][1]
                   
               }]
               
                for bill_check in bill.bill_check_ids:
                   transfer_history.insert(0,{
                        'date': bill_check.date,
                        'name': next(_c[1] for _c in _bill_selection if bill_check.check_type == _c[0]), 
                        'processor': bill_check.user_id.name,
                        'bgcolor': random.choice(badge_color),
                        'icon': next(_c[1] for _c in _icon_selection if bill_check.check_type == _c[0])
                   })
                   
                
        
               
               # search the check of this bill
                
                return {
                   'id': bill.id,
                   'name': bill.name,
                   'packing_code': bill.packing_code,
                   'bill_date': bill.bill_date,
                   'done_date': bill.done_date,
                    'customer_id': bill.customer_id.name,
                    'customer_address': bill.customer_address,
                    'customer_mobile': bill.customer_mobile,
                    'package_weight': bill.package_weight,
                    'unit_price': bill.unit_price,
                    'unit_quantity': bill.unit_quantity,
                    'total_amount': bill.total_amount,
                    'note': bill.note,
                   'origin_code': bill.origin_code,
                   'goods_name': bill.goods_name,
                   'state': next(stt[1] for stt in _bill_selection if stt[0] == bill.state),
                   'color': next(c[1] for c in _color_selection if c[0] == bill.state),
                   'transfer_history': transfer_history or []
               } 
        
        return {}