# -*- coding: utf-8 -*-
# from odoo import http


# class SmartApps(http.Controller):
#     @http.route('/smart_apps/smart_apps/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/smart_apps/smart_apps/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('smart_apps.listing', {
#             'root': '/smart_apps/smart_apps',
#             'objects': http.request.env['smart_apps.smart_apps'].search([]),
#         })

#     @http.route('/smart_apps/smart_apps/objects/<model("smart_apps.smart_apps"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('smart_apps.object', {
#             'object': obj
#         })
