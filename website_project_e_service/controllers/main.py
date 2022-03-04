# -*- coding: utf-8 -*-
from dbus import MissingErrorHandlerException
from odoo import fields, http, _
from odoo.http import request
from collections import OrderedDict
from odoo.exceptions import MissingError
from odoo.addons.website.controllers.main import QueryURL
import logging
from collections import deque
import io
import json
from odoo.tools import ustr
from odoo.tools.misc import xlsxwriter

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

    @http.route(['''/download/e-service/<int:project_id>'''], type='http', auth="public", website=True)
    def download_project_e_service(self, project_id):
        if project_id:
            project_obj_id = request.env['project.project'].sudo().browse(project_id)

            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet()
            row = 0
            col = 0

            # ~ header = ['Name', 'E-Service Form','Service Category/E-Service/Name','Require Login','Is e-service','Icon']
            header = ['Name', 'E-Service Form','Service Category/E-Service/Name','Require Login','Is e-service']
            for data in header:
                _logger.warning(f"{data=}")
                worksheet.write(row, col, data)
                col += 1
            col = 0

            for project in project_obj_id:
                # ~ item = [project.name, project.e_service_form,project.e_service_category.name,project.require_login,project.is_e_service,project.e_service_icon]
                item = [project.name, project.e_service_form,project.e_service_category.name,project.require_login,project.is_e_service]
                for data in item:
                    if data == project.e_service_icon:
                        worksheet.insert_image(row, col, data)
                    else:
                        worksheet.write(row, col, data)
                    col += 1
                col = 0
            workbook.close()
            xlsx_data = output.getvalue()
            response = request.make_response(xlsx_data,
                                             headers=[('Content-Type',
                                                       'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                                                      ('Content-Disposition', 'attachment; filename=%s.xlsx'
                                                       % project_obj_id.name)])

            return response


    @http.route(['/e-service/portal/accept'], type='json', auth="public", website=True)
    def _eservice_portal_accept(self, partner_id=None, task_id=None,failed=False, **kwargs):
        task = request.env['project.task'].sudo().browse(int(task_id))
        template_id = request.env['ir.model.data'].get_object_reference(
                    'eservice_portal_accept',
                    'email_template_eservice_portal_accept')[1]
        if template_id:
            template = self.env['mail.template'].browse(template_id)
            values = template.generate_email(task.id, ['subject', 'body_html', 'email_from', 'email_to', 'partner_to', 'email_cc', 'reply_to', 'scheduled_date'])
            msg_id = self.env['mail.mail'].create(values)
            if msg_id:
                msg_id._send()

        return {'result': True}
