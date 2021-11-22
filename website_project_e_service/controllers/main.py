# -*- coding: utf-8 -*-

import collections
import babel.dates
import re
import werkzeug
from werkzeug.datastructures import OrderedMultiDict
from werkzeug.exceptions import NotFound

from ast import literal_eval
from collections import defaultdict
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import fields, http, _
from odoo.addons.website_event.controllers.main import WebsiteEventController
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.event.controllers.main import EventController
from odoo.http import request
from odoo.osv import expression
from odoo.tools.misc import get_lang, format_date


class ProjectEServiceController(http.Controller):

    @http.route(['/e-services', '/e-services/page/<int:page>'], type='http', auth="public", website=True)
    def project_e_services(self, page=1, **searches):
        project_ids = request.env['project.project'].sudo().search([('is_e_service', '=', True)])

        searches.setdefault('search', '')
        searches.setdefault('category', 'all')

        values = {
            'project_ids': project_ids
        }

        return request.render("website_project_e_service.index", values)

    @http.route(['''/e-service/<model("project.project"):project>'''], type='http', auth="public", website=True)
    def project_e_service(self, project, **searches):
        values = {
            'project': project.sudo()
        }

        return request.render("website_project_e_service.e_service_description_full", values)
