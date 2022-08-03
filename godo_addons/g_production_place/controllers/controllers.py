# -*- coding: utf-8 -*-
# from odoo import http


# class GodoAddons/gProductionPlace(http.Controller):
#     @http.route('/godo_addons/g_production_place/godo_addons/g_production_place', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/godo_addons/g_production_place/godo_addons/g_production_place/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('godo_addons/g_production_place.listing', {
#             'root': '/godo_addons/g_production_place/godo_addons/g_production_place',
#             'objects': http.request.env['godo_addons/g_production_place.godo_addons/g_production_place'].search([]),
#         })

#     @http.route('/godo_addons/g_production_place/godo_addons/g_production_place/objects/<model("godo_addons/g_production_place.godo_addons/g_production_place"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('godo_addons/g_production_place.object', {
#             'object': obj
#         })
