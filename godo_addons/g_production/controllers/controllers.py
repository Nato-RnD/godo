# -*- coding: utf-8 -*-
# from odoo import http


# class GodoAddons/gProduction(http.Controller):
#     @http.route('/godo_addons/g_production/godo_addons/g_production', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/godo_addons/g_production/godo_addons/g_production/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('godo_addons/g_production.listing', {
#             'root': '/godo_addons/g_production/godo_addons/g_production',
#             'objects': http.request.env['godo_addons/g_production.godo_addons/g_production'].search([]),
#         })

#     @http.route('/godo_addons/g_production/godo_addons/g_production/objects/<model("godo_addons/g_production.godo_addons/g_production"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('godo_addons/g_production.object', {
#             'object': obj
#         })
