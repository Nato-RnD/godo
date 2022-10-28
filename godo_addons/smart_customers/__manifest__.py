# -*- coding: utf-8 -*-
{
    'name': "Customers & Services",

    'summary': """
        This smart customers handle customer of smartlife 
        """,

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

    # any module necessary for this one to work correctly
    'depends': ['base','g_init','product', 'sale'],
    'application':True,

    # always loaded
    'data': [
        
        'views/assets.xml', 
        'security/ir.model.access.csv',
        'views/service_config_views.xml', 
        'views/res_account_views.xml',
        'views/res_partner_views.xml',
        'views/overview_dashboard_template.xml', 
        'views/res_sm_wallet_views.xml',
        'views/res_sm_transaction_views.xml',
        'views/product_template_views.xml',
        'views/product_pricelist_views.xml',
        'views/res_sm_contract.xml',
        'reports/contract_report_template.xml',
        'reports/contract_report.xml',
        'views/menu.xml', 
    ],
    'qweb': [
        'static/src/xml/building_dashboard.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
