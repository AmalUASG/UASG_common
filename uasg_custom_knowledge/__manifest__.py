# -*- coding: utf-8 -*-
{
    'name': "UASG Custom Knowledge",

    'summary': """
        This module is providing a custom module for knowledge base Management 

""",

    'description': """
       This module is providing a custom module for knowledge base Management   
    """,

    'author': "UASG/amal.abdelmajid",
    'website': "https://www.alsaqergroup.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customizations',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'uasg_custom_budget ' ],

    # always loaded
    'data': [
      
        'views/view.xml',
 
    ],    

}
