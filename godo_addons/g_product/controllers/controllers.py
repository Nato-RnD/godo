# -*- coding: utf-8 -*-
# from odoo import http


# class GProduct(http.Controller):
#     @http.route('/g_product/g_product', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/g_product/g_product/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('g_product.listing', {
#             'root': '/g_product/g_product',
#             'objects': http.request.env['g_product.g_product'].search([]),
#         })

#     @http.route('/g_product/g_product/objects/<model("g_product.g_product"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('g_product.object', {
#             'object': obj
#         })
