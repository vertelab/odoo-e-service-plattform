# -*- coding: utf-8 -*-
{
    'name': "partner_navet",

    'summary': """Imports people from Navet into odoo res partners.""",

    'description': '''
partner_navet
=============

    Imports people from Navet into odoo res partners.

    Features:

        - UI Integration: Extends 1 view(s) in the Odoo interface.
        - Extends Odoo: Builds on navet.import, partner.navet.import.
    ''',

    'author': "Vertel AB",
    'website': "https://vertel.se/apps/odoo-e-service-plattform/partner_navet",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Contact',
    'version': '18.0.0.2.0',
    'license': 'AGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['contacts'],

    # always loaded
    'data': [
        'data/navet_import.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
}
