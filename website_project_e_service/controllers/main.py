# -*- coding: utf-8 -*-
from dbus import MissingErrorHandlerException
from odoo import fields, http, _
from odoo.http import request
from collections import OrderedDict
from odoo.exceptions import MissingError
from odoo.addons.website.controllers.main import QueryURL
import logging

_logger = logging.getLogger(__name__)


class ProjectEServiceController(http.Controller):

    @http.route(['/e-services', '/e-services/page/<int:page>'], type='http', auth="public", website=True)
    def project_e_services(self, page=1, **searches):
        website = request.website
        e_service_ids = request.env['project.e_service.category'].sudo()

        current_e_category = None

        domain = [('project_id', '!=', False)]

        if searches.get('search'):
            domain += [('name', 'ilike', searches['search'])]
            e_service_ids = e_service_ids.search(domain)
        elif searches.get('e_category'):
            domain += [('e_service_id', '=', int(searches['e_category']))]
            e_service_ids = e_service_ids.search(domain)
        else:
            e_service_ids = e_service_ids.search(domain)

        step = 12  # Number of events per page
        service_count = e_service_ids.search_count(domain)

        e_service_list = []
        for _rec in e_service_ids:
            e_service_list.append({
                'e_service_id': _rec.e_service_id,
                'project_ids': _rec.project_id
            })

        _e_categories_items = OrderedDict()
        for items in e_service_list:
            _e_categories_items.setdefault(
                items['e_service_id'], []).append(items['project_ids'])

        e_service_ids = [{'e_service_id': k,  'project_ids': set(
            v)} for k, v in _e_categories_items.items()]

        pager = website.pager(
            url="/e-services",
            url_args=searches,
            total=service_count,
            page=page,
            step=step,
            scope=5)

        searches.setdefault('search', '')
        searches.setdefault('e_category', 'all')

        keep = QueryURL('/e-services',
                        **{key: value for key, value in searches.items() if (key == 'search' or value != 'all')})

        values = {
            'e_service_ids': e_service_ids,
            'pager': pager,
            'current_e_category': current_e_category,
            'keep': keep,
            'searches': searches,
        }
        return request.render("website_project_e_service.index", values)

    @http.route(['''/e-service/<string:form>'''], type='http', auth="public", website=True)
    def project_e_service(self, form, **searches):
        id = 0
        if '-' in form:
            id = int(form.split('-')[-1])
        project = request.env['project.project'].sudo().browse(id)
        if not project.exists():
            return self.project_e_services()
        if project.require_login and not request.env.context.get('uid'):
            return request.redirect('/web/login?redirect=/e-service/' + form)
        _logger.error(f"{request.env.context=}")
        view = 'website_project_e_service.e_service_description_full'
        return request.render(view, {'project': project})
