# -*- coding: utf-8 -*-
{
    'name': "SQL Odoo Connector",

    'summary': """
        This module is providing SQL odoo connector   

""",

    'description': """
         This module is providing SQL odoo connector          
    """,

    'author': "UASG",
    'website': "https://www.alsaqergroup.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customizations',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base' ],

    # always loaded
    'data': [
      'security/ir.model.access.csv',
        'views.xml',

 
    ], 

     'assets': {
        'web.assets_backend': [
            'uasg_custom_user_menu/static/src/js/menu.js']}
    

}
