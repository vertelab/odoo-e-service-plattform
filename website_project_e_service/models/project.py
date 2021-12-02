from odoo import models, api, fields, _
from odoo.tools.translate import html_translate
from odoo.tools import html2plaintext


class Project(models.Model):
    _inherit = 'project.project'
    e_service_form = fields.Html()

    @api.model
    def create_project_portal(self, values):
        if not (values['project_name'] and values['e_service_id']):
            return {
                'errors': _('All fields are required !')
            }

        project_id = self.create({
            'name': values['project_name'],
            'e_service_category': [
                (0, 0, {'e_service_id': int(values['e_service_id'])})
            ],
            'is_e_service': True
        })
        return {
            'id': project_id.id
        }
