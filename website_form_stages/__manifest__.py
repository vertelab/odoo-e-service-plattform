# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo SA, Open Source Management Solution, third party addon
#    Copyright (C) 2021- Vertel AB (<https://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Website Form Stages',
    'summary': 'Adds a snippet that creates a form with stages.',
    'author': 'Vertel AB',
    'category': 'Project',
    'version': '18.0.0.0.1',
    'license': 'AGPL-3',
    'website': 'https://vertel.se/apps/odoo-e-service-plattform/website_form_stages',
    'description': '''
Website Form Stages
===================

    Adds a snippet that creates a form with stages.

    Features:

        - UI Integration: Extends 2 view(s) in the Odoo interface.
    ''',
    'depends': ['website','mail','google_recaptcha'],
    'data': [
        'views/template.xml',
        'views/website_form_stages.xml',
    ],
    'application': True,
    'installable': True,
}
