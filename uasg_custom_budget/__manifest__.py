# -*- coding: utf-8 -*-
{
    'name': "UASG Budget",

    'summary': """
     Customization for UASG Budget

        """,

    'description': """
        Customization for UASG Budget
    """,

    'author': "UASG / Amal Abelmajid",
    'website': "https://www.alsaqergroup.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','uasg_custom_contacts'],

    # always loaded
    'data': [
        'data/data.xml',
        'security/budget_security.xml',
        'security/ir.model.access.csv',
        'reports/budget_report_view.xml',
        'views/views.xml',
        'views/templates.xml',
        
        'views/res_users.xml',

    ],

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',


    ],

    'installable': True,
    'application': True,
}
