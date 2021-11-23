# -*- coding: utf-8 -*-

from odoo import fields, http, _
from odoo.http import request


class ProjectEServiceController(http.Controller):

    @http.route(['/e-services', '/e-services/page/<int:page>'], type='http', auth="public", website=True)
    def project_e_services(self, page=1, **searches):
        website = request.website
        project_ids = request.env['project.project'].sudo()
        domain = [('is_e_service', '=', True)]

        if searches.get('search'):
            domain += [('name', 'ilike', searches['search'])]
            project_ids = project_ids.search(domain)
        else:
            project_ids = project_ids.search(domain)

        step = 12  # Number of events per page
        project_count = project_ids.search_count(domain)

        pager = website.pager(
            url="/e-services",
            url_args=searches,
            total=project_count,
            page=page,
            step=step,
            scope=5)

        searches.setdefault('search', '')
        searches.setdefault('category', 'all')

        values = {
            'project_ids': project_ids,
            'pager': pager,
        }

        return request.render("website_project_e_service.index", values)

    @http.route(['''/e-service/<model("project.project"):project>'''], type='http', auth="public", website=True)
    def project_e_service(self, project, **searches):
        values = {
            'project': project.sudo()
        }

        return request.render("website_project_e_service.e_service_description_full", values)
