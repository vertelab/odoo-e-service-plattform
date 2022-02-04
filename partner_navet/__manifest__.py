# -*- coding: utf-8 -*-
{
    'name': "partner_navet",

    'summary': """
        Imports people from Navet into odoo res partners
    """,

    'description': """
        Imports people from Navet into odoo res partners
    """,

    'author': "Vertel AB",
    'website': "http://www.vertel.se",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Contact',
    'version': '14.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['contacts'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
}
