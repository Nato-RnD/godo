# -*- coding: utf-8 -*-
from odoo import http 
class GPucPortal(http.Controller):  
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
        
    @http.route(['/my', '/my/tokhai-kythuat'], type='http', auth="user", website=True)
    def home(self, **kw):
        values = self._prepare_portal_layout_values()
        _declarations = http.request.env['godo.production.unit.declaration'].search([('registered_user_id','=',http.request.env.user.id)])
        # decl = []
        # for model in _declarations:
        #     decl.append(model.read())
        values['test'] = _declarations
        return http.request.render("g_production_place.portal_layout", values)

 
    @http.route(['/my/tokhai-kythuat/detail/<int:declaration_id>'], type='http', auth="user", website=True)
    def declaration_detail(self,declaration_id, **kw):
        values = self._prepare_portal_layout_values()
        _declaration = http.request.env['godo.production.unit.declaration'].browse(declaration_id)
        # decl = []
        # for model in _declarations:
        #     decl.append(model.read())
        values['detail'] = _declaration
        return http.request.render("g_production_place.portal_layout", values)

 