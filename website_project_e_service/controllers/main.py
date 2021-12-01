# -*- coding: utf-8 -*-

from odoo import fields, http, _
from odoo.http import request
from collections import OrderedDict
from odoo.addons.website.controllers.main import QueryURL


class ProjectEServiceController(http.Controller):

    @http.route(['/e-services', '/e-services/page/<int:page>'], type='http', auth="public", website=True)
    def project_e_services(self, page=1, **searches):
        website = request.website
        project_ids = request.env['project.project'].sudo()
        domain = [('is_e_service', '=', True)]

        current_e_category = None

        if searches.get('search'):
            domain += [('name', 'ilike', searches['search'])]
            project_ids = project_ids.search(domain)
        elif searches.get('e_category'):
            project_e_service_ids = request.env['project.e_service.category'].search([('e_service_id', '=', int(searches['e_category']))])
            project_ids = project_e_service_ids.mapped('project_id')
            current_e_category = request.env['e_service.category'].browse(int(searches['e_category']))
        else:
            project_ids = project_ids.search(domain)

        step = 12  # Number of events per page
        project_count = project_ids.search_count(domain)

        e_categories = request.env['project.e_service.category'].search([])

        e_categories_items = []

        for rec in e_categories:
            if rec.project_id:
                e_categories_items.append({
                    'e_category_id': rec.e_service_id,
                    'e_category_id_count': 1
                })

        _e_categories_items = OrderedDict()
        for items in e_categories_items:
            _e_categories_items.setdefault(items['e_category_id'], []).append(items['e_category_id_count'])

        e_categories_items = [{'e_category_id': k,  'e_category_id_count': sum(v)} for k, v in _e_categories_items.items()]

        pager = website.pager(
            url="/e-services",
            url_args=searches,
            total=project_count,
            page=page,
            step=step,
            scope=5)

        searches.setdefault('search', '')
        searches.setdefault('e_category', 'all')

        keep = QueryURL('/event',
                        **{key: value for key, value in searches.items() if (key == 'search' or value != 'all')})

        values = {
            'project_ids': project_ids,
            'pager': pager,
            'e_categories': e_categories_items,
            'current_e_category': current_e_category,
            'keep': keep,
            'searches': searches,
        }
        return request.render("website_project_e_service.index", values)

    @http.route(['''/e-service/<string:form>'''], type='http', auth="public", website=True)
    def project_e_service(self, form, **searches):
        id = int(form.split('-')[-1])
        project = request.env['project.project'].sudo().browse(id)
        values = {'project': project}

        return request.render("website_project_e_service.e_service_description_full", values)
