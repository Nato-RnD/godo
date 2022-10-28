# -*- coding: utf-8 -*-
# from odoo import http


# class SmartCustomers(http.Controller):
#     @http.route('/smart_customers/smart_customers/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/smart_customers/smart_customers/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('smart_customers.listing', {
#             'root': '/smart_customers/smart_customers',
#             'objects': http.request.env['smart_customers.smart_customers'].search([]),
#         })

#     @http.route('/smart_customers/smart_customers/objects/<model("smart_customers.smart_customers"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('smart_customers.object', {
#             'object': obj
#         })
