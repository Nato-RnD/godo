# -*- coding: utf-8 -*-
{
    'name': "G Logistics",

    'summary': """
      Hệ thống quản lý về vận đơn trong chuỗi logistic
      """,

    'description': """
       Hệ thống quản lý về vận đơn trong chuỗi logistic
    """,

    'author': "My Company",
    'website': "http://smartlifevn.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'G Office',
    'version': '0.1',
    'application': True,
    # any module necessary for this one to work correctly
    'depends': ['base','mail','web','g_partner'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/bill_views.xml',
        'views/check_views.xml',
        'views/menu_views.xml',
         
    ],
    'assets': {
        'web.assets_backend': [ 
            
        ]
        
      }
 
}
