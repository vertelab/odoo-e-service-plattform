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
    'summary': 'To be able to create e-service from website',
    'author': 'Vertel AB',
    'category': 'Project',
    'version': '14.0.0.0.1',
    'website': 'https://vertel.se',
    'description': """
        14.0.0.0.1 - Initial Development
    """,
    'depends': ['website', 'web_editor', 'project_e_service'],
    'data': [
        'views/assets.xml',
        'views/website_navbar_templates.xml',
        'views/e_service_template.xml',
        'views/e_service_description.xml',
    ],
    'application': True,
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4s:softtabstop=4:shiftwidth=4:
