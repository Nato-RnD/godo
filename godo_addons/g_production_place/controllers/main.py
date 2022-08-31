# -*- coding: utf-8 -*-
from odoo.http import route,request 
from odoo.addons.portal.controllers.portal import CustomerPortal
class GPucPortal(CustomerPortal):  
    def _prepare_portal_layout_values(self):
        """Values for /my/* templates rendering.

        Does not include the record counts.
        """
        # get customer sales rep
        sales_user = False
        partner = request.env.user.partner_id
        if partner.user_id and not partner.user_id._is_public():
            sales_user = partner.user_id

        return {
            'sales_user': sales_user,
            'page_name': 'home',
        }
        
    @route(['/my', '/my/productions'], type='http', auth="user", website=True)
    def declaration_list(self, **kw):
        values = self._prepare_portal_layout_values()
        _declarations = request.env['godo.production.unit.declaration'].sudo().search([('registered_user_id','=',request.env.user.id)]) 
        values.update({
            'listview': True,
            'declaration_list': _declarations,
            'page_name': 'declaration' 
        })
        response = request.render("g_production_place.portal_my_puc_listview", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response 

 
    @route(['/my/productions/detail/<int:declaration_id>'], type='http', auth="user", website=True)
    def declaration_detail(self,declaration_id, **kw):
        values = self._prepare_portal_layout_values()
        _declaration = request.env['godo.production.unit.declaration'].browse(declaration_id)
        values['detailview'] = True
        values['declaration_detail'] = _declaration
        values.update({ 
            'declaration_detail': _declaration,
            'page_name': 'detail' 
        })
        response = request.render("g_production_place.portal_my_puc_detailview", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response 
     

    @route(['/my/productions/edit/<int:declaration_id>'], type='http', auth="user", website=True)
    def declaration_edit(self,declaration_id, **kw):
        values = self._prepare_portal_layout_values()
        _declaration = request.env['godo.production.unit.declaration'].browse(declaration_id)
        values.update({ 
            'declaration_detail': _declaration,
            'page_name': 'edit' 
        })
        response = request.render("g_production_place.portal_my_puc_detailview", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    
    @route(['/my/productions/register'], type='http', auth="user", website=True)
    def declaration_register(self, **kw):
        values = self._prepare_portal_layout_values()
        # _declaration = request.env['godo.production.unit.declaration'].browse(declaration_id) 
        values.update({  
            'page_name': 'create' 
        })
        return request.render("g_production_place.portal_my_puc_create_view", values)


    @route(['/my/account'], type='http', auth='user', website=True)
    def account(self, redirect=None, **post):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        values.update({
            'error': {},
            'error_message': [],
        })

        if post and request.httprequest.method == 'POST':
            error, error_message = self.details_form_validate(post)
            values.update({'error': error, 'error_message': error_message})
            values.update(post)
            if not error:
                values = {key: post[key] for key in self.MANDATORY_BILLING_FIELDS}
                values.update({key: post[key] for key in self.OPTIONAL_BILLING_FIELDS if key in post})
                for field in set(['province_id', 'district_id']) & set(values.keys()):
                    try:
                        values[field] = int(values[field])
                    except:
                        values[field] = False
                # values.update({'zip': values.pop('zipcode', '')})
                partner.sudo().write(values)
                if redirect:
                    return request.redirect(redirect)
                return request.redirect('/my/home')

        provinces = request.env['res.province'].sudo().search([])
        districts = request.env['res.district'].sudo().search([])
        wards = request.env['res.ward'].sudo().search([])

        values.update({
            'partner': partner,
            'provinces': provinces,
            'districts': districts,
            'wards': wards,
            'has_check_vat': hasattr(request.env['res.partner'], 'check_vat'),
            'redirect': redirect,
            'page_name': 'my_details',
        })

        response = request.render("portal.portal_my_details", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response
 

    @route(['/my', '/my/home'], type='http', auth="user", website=True)
    def home(self, **kw):
        values = self._prepare_portal_layout_values()
        return request.render("portal.portal_my_home", values)