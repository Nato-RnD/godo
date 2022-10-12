# -*- coding: utf-8 -*-
{
    'name': "G PUC",

    'summary': """
       Quản lý vùng trồng
        """,

    'description': """
       Quản lý vùng trồng
    """,

    'author': "Smartlife Software R&D Dept.",
    'website': "http://smartlifevn.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'G-Office',
    'version': '0.1',
    'license':'LGPL-3',
    'application':True,

    # any module necessary for this one to work correctly
    'depends': ['base','g_production','g_partner','portal'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/production_pest_views.xml',
        'views/production_puc_code_views.xml',
        'views/production_puc_declaration_views.xml',
        'views/production_puc_inspection_views.xml',
        'views/portal_layout_template.xml',
        'views/production_puc_declaration_template.xml',
        'views/production_puc_target_country_views.xml',
        'views/menu_views.xml',
    ],
    
    'assets': {
        'web.assets_backend': [
            'g_production_place/static/src/css/map.css',
            'g_production_place/static/src/vendors/leaflet/leaflet.css',
            'g_production_place/static/src/vendors/leaflet/leaflet.js',
            'g_production_place/static/src/js/map.js', 
        ],
    'web.assets_qweb': [
            'g_production_place/static/src/xml/**/*',
           
        ],
    'web.assets_frontend': [ 
            'g_production_place/static/src/js/portal.js', 
        ],
    },
 
}
