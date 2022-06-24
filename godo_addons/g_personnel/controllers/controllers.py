# -*- coding: utf-8 -*-
# from odoo import http


# class GPersonnel(http.Controller):
#     @http.route('/g_personnel/g_personnel', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/g_personnel/g_personnel/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('g_personnel.listing', {
#             'root': '/g_personnel/g_personnel',
#             'objects': http.request.env['g_personnel.g_personnel'].search([]),
#         })

#     @http.route('/g_personnel/g_personnel/objects/<model("g_personnel.g_personnel"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('g_personnel.object', {
#             'object': obj
#         })
