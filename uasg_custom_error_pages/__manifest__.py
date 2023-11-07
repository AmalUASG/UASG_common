# -*- coding: utf-8 -*-
{
    'name': "UASG Custom Error Pages",

    'summary': """
        This module is providing customization on errors pages        

""",

    'description': """
      This module is providing customization on errors pages        
  
    """,

    'author': "UASG",
    'website': "https://www.alsaqergroup.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customizations',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base' ,'http_routing'],

    # always loaded
    'data': [
      
        'views/403.xml',
 
    ], 
 

}
