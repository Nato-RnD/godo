# -*- coding: utf-8 -*-
{
    'name': "G Init",

    'summary': """
      Module cài đặt địa danh hành chính Vn 
        """,

    'description': """
        Module cài đặt địa danh hành chính Vn 
    """,

    'author': "Smartlife Software R&D Dept.",
    'website': "http://smartlifevn.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'godo',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],
    'auto_install': True,

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/province.xml',
        'data/district.xml',
        'data/ward.xml', 
    ],

    'assets':{
          'web.assets_backend': [
                'g_init/static/src/js/widgets.js',
                'g_init/static/src/js/lightbox.js',
                  'g_init/static/src/css/lightbox.css',
          ]
    }
    # only loaded in demonstration mode
    
}
