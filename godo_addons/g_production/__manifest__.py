# -*- coding: utf-8 -*-
{
    'name': "G Production",

    'summary': """
       Quản lý sản phẩm và nhóm sản phẩm, các nhóm cây trồng
       """,

    'description': """
      Quản lý sản phẩm và nhóm sản phẩm, các nhóm cây trồng
    """,

    'author': "Smartlife Software R&D Dept.",
    'website': "http://smartlifevn.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'G office',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','web','product'],
    'license':'LGPL-3',
    'application':True,
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/production.xml',
        'views/production_views.xml', 
        'views/fertilizer_views.xml', 
        'views/pesticides_views.xml', 
        'views/product_views.xml', 
        'views/menu_views.xml',
    ],
    # only loaded in demonstration mode
  
}
