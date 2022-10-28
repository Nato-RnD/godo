# -*- coding: utf-8 -*-
{
    'name': "Apps Register",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Smartlife Software R&D Dept",
    'website': "http://smartlifevn.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Smartlife',
    'version': '0.1',
    "application":True,

    # any module necessary for this one to work correctly
    'depends': ['base','mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_apps_views.xml',
        'views/menu.xml',
    ], 
}
