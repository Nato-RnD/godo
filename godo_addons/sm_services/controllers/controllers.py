# -*- coding: utf-8 -*-
# from odoo import http


# class SmServices(http.Controller):
#     @http.route('/sm_services/sm_services', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sm_services/sm_services/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sm_services.listing', {
#             'root': '/sm_services/sm_services',
#             'objects': http.request.env['sm_services.sm_services'].search([]),
#         })

#     @http.route('/sm_services/sm_services/objects/<model("sm_services.sm_services"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sm_services.object', {
#             'object': obj
#         })
