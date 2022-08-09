from odoo import http
from odoo.http import request

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
       ( 'sent', 'alert alert-warning'),
       ( 'received', 'alert alert-info'),
       ( 'forward','alert alert-danger'),
       ( 'done', 'alert alert-success'),
       ( 'cancelled','alert alert-secondary')
    ] 
        bill_code = kw.get('code',None)
        if bill_code is not None:
           bill = request.env['godo.logistic.bill'].search(['|',('origin_code','=',bill_code),('name','=',bill_code)],limit=1)
           if bill: 
               return {
                   'id': bill.id,
                   'name': bill.name,
                   'packing_code': bill.packing_code,
                   'bill_date': bill.bill_date,
                   'done_date': bill.done_date,
                    'customer_id': bill.customer_id,
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
                   'color': next(c[1] for c in _color_selection if c[0] == bill.state)
               } 
        
        return {}