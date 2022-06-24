# -*- coding: utf-8 -*-
{
    'name': "Nhân sự",

    'summary': """
       Đây là module về quản lý nhân sự trong cơ quan
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Smartlife Software R&D Dept.",
    'website': "http://smartlifevn.com", 
    'category': 'G-Office',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/menu_views.xml', 
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
