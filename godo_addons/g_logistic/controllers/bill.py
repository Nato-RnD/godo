from odoo import http
from odoo.http import request
from odoo.models import _
class BillSearch(http.Controller):
   @http.route(['/bill-search'], type="json", auth="public")
   def bill_search(self, **kw):
         _bill_selection = [
       ( 'draft',_('Order'), _('The order has created')),
       ( 'delivery',_('Delivery from Shop'), _('The goods has deliveried from Shop')),
       ( 'fullfil',_('Fulfillment'), _('The goods has fulfilled to warehouse in China')),
       ( 'sent',_('Sent from China'), _('The goods has sent from China')),
       ( 'received',_('Received'), _('Vietnam warehouse has received the goods')),
       ( 'forward',_('Forwarded'),_('Delivered via third-party')),
       ( 'done', _('Done'),_('Customer has received the goods')),
       ( 'cancelled',_('Cancelled'),_('The bill has been cancelled'))
    ] 
         _color_selection =   [
       ( 'draft', 'alert alert-warning'),
       ( 'delivery', 'alert alert-info'),
       ( 'fullfil', 'alert alert-secondary'),
       ( 'sent', 'alert alert-primary'),
       ( 'received', 'alert alert-info'),
       ( 'forward','alert alert-danger'),
       ( 'done', 'alert alert-success'),
       ( 'cancelled','alert alert-secondary')
    ]
         _icon_selection =   [
        ( 'draft', 'fa fa-shopping-cart'),
         ( 'delivery', 'fa fa-truck'),
         ( 'fullfil', 'fa fa-database'),
       ( 'sent', 'fa fa-send'),
       ( 'received', 'fa fa-calendar-check-o'),
       ( 'forward','fa fa-truck'),
       ( 'done', 'fa fa-map-signs'),
       ( 'cancelled','fa fa-lock')
    ]
         
         bill_code = kw.get('code',None)
         if bill_code is not None:
            bill = request.env['godo.logistic.bill'].sudo().search(['|',('name','=',bill_code),('origin_code','=', bill_code)],limit=1)
            print(bill)
            if bill: 
               transfer_history = [] 
              #  #[{ 
              #      'date': bill.bill_date,
              #      'name': self._find__array(_bill_selection,bill.state)[2] or '', #_bill_selection[0][2], 
              #      'bgcolor': '',
              #      'icon':  self._find__array(_icon_selection,bill.state)[1] or None #  [0][1]
                   
              #  }]
               
               i = 0
               for bill_check in bill.bill_check_ids:
                   if i == 0:
                      transfer_history.insert(0,{
                        'date': bill.bill_date,
                        'name': _bill_selection[_bill_selection.index(self._find__array(_bill_selection,bill_check.check_type))-1][2] or None , # next(_c[2] for _c in _bill_selection if bill_check.check_type == _c[0]), 
                        'processor': bill_check.user_id.name,
                        'bgcolor':'',
                        'icon': _icon_selection[_icon_selection.index(self._find__array(_icon_selection,bill_check.check_type))-1][1] #next(_c[1] for _c in _icon_selection if bill_check.check_type == _c[0])
                      })
                         
                   transfer_history.insert(0,{
                        'date': bill_check.date,
                        'name':  next(_c[2] for _c in _bill_selection if bill_check.check_type == _c[0]), #self._find__array(_bill_selection,bill_check.check_type)[2] , #
                        'processor': bill_check.user_id.name,
                        'bgcolor':'',
                        'icon': next(_c[1] for _c in _icon_selection if bill_check.check_type == _c[0]) #self._find__array(_icon_selection,bill_check.check_type)[1]  #
                   })
                   i = i+1
                   
               if len(transfer_history) == 0:
                    transfer_history.insert(0,{
                        'date': bill.bill_date,
                        'name': self._find__array(_bill_selection,bill.state)[2] ,
                        'bgcolor':'',
                        'icon': self._find__array(_icon_selection,bill.state)[1]
                      })
                    
               transfer_history[0]['bgcolor']='bg-success' if len(transfer_history)>0 else {}
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
       
   def  _find__array(self,array,state):
        return next( item  for item in array if item[0] ==state)
      
  #  def  _find__previous_index_array(self,array,state):
  #        i = 0
  #        for st in array:
  #           if st[0] == state:
  #             return               
         
  #       index = next( item  for item in array if item[0] ==state)
    