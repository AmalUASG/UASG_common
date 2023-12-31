# -*- coding: utf-8 -*-
{
    'name': "UASG Project",

    'summary': """
            Customization for UASG Project
""",

    'description': """
            Customization for UASG Project

    """,

    'author': "UASG / Amal Abelmajid",
    'website': "https://www.alsaqergroup.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','uasg_custom_contacts'],

    # always loaded
    'data': [
        'data/data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/res_partner.xml',
        'views/templates.xml',
    ],
    
    'installable': True,
    'application': True,
}
