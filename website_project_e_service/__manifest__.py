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
    'name': 'Website Project E-Service',
    'summary': 'To be able to create e-service from website.',
    'author': 'Vertel AB',
    'category': 'Project',
    'version': '18.0.0.1.0',
    'license': 'AGPL-3',
    'website': 'https://vertel.se/apps/odoo-e-service-plattform/website_project_e_service',
    'description': '''
Website Project E-Service
=========================

    14.0.0.2.0 - Add autofill for input fields
            14.0.0.1.0 - Add Skolskjuts-form
            14.0.0.0.1 - Initial Development

    Features:

        - Web integration: Exposes HTTP endpoints for external systems.
        - Guided Wizards: Step-by-step dialogs for data entry.
        - UI Integration: Extends 5 view(s) in the Odoo interface.
        - Extends Odoo: Builds on project.project.
    ''',
    'depends': ['freja_partner_navet', 'project_e_service', 'website_form'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/project_wizard.xml',
        'data/e-service_config.xml',
        'data/project.xml',
        'data/website_menu.xml',
        'data/e_service.category.csv',
        'data/project.e_service.category.csv',
        'views/assets.xml',
        'views/website_navbar_templates.xml',
        'views/e_service_template.xml',
        'views/e_service_description.xml',
        'views/e_service_snippet.xml',
        'views/snippets/snippets.xml',
    ],
    'application': True,
    'installable': True,
}
