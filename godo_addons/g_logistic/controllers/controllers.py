# -*- coding: utf-8 -*-
# from odoo import http


# class GodoAddons/gLogistic(http.Controller):
#     @http.route('/godo_addons/g_logistic/godo_addons/g_logistic', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/godo_addons/g_logistic/godo_addons/g_logistic/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('godo_addons/g_logistic.listing', {
#             'root': '/godo_addons/g_logistic/godo_addons/g_logistic',
#             'objects': http.request.env['godo_addons/g_logistic.godo_addons/g_logistic'].search([]),
#         })

#     @http.route('/godo_addons/g_logistic/godo_addons/g_logistic/objects/<model("godo_addons/g_logistic.godo_addons/g_logistic"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('godo_addons/g_logistic.object', {
#             'object': obj
#         })
