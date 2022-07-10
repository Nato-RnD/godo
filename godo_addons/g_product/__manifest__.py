# -*- coding: utf-8 -*-
{
    'name': "G products",

    'summary': """
       Quản lý sản phẩm và nhóm sản phẩm
       """,

    'description': """
      Quản lý sản phẩm và nhóm sản phẩm
    """,

    'author': "Smartlife Software R&D Dept.",
    'website': "http://smartlifevn.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'G office',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv', 
    ],
 
}
