# -*- coding: utf-8 -*-
{
    'name': "G partner",

    'summary': """
        Quản lý đối tác của đơn vị
        """,

    'description': """
          Quản lý đối tác của đơn vị
    """,

    'author': "SmartLife Software R&D Dept.",
    'website': "http://smartlifevn.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'G-Office',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/portal_views.xml', 
    ],
    # only loaded in demonstration mode
 
}
