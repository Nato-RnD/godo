# -*- coding: utf-8 -*-
from odoo import http 
class GPartnerPortal(http.Controller): 
    
    
    def _prepare_portal_layout_values(self):
        """Values for /my/* templates rendering.

        Does not include the record counts.
        """
        # get customer sales rep
        sales_user = False
        partner = http.request.env.user.partner_id
        if partner.user_id and not partner.user_id._is_public():
            sales_user = partner.user_id

        return {
            'sales_user': sales_user,
            'page_name': 'home',
        }
        
    @http.route(['/my', '/my/products'], type='http', auth="user", website=True)
    def home(self, **kw):
        values = self._prepare_portal_layout_values()
        return http.request.render("g_partner.portal_my_product", values)