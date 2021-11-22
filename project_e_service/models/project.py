from odoo import models, api, fields, _
from odoo.tools.translate import html_translate
from odoo.tools import html2plaintext


class Project(models.Model):
    _inherit = 'project.project'

    is_e_service = fields.Boolean(string="Is e-service")
    e_service_category = fields.One2many('project.e_service.category', 'project_id', string="Service Category")
    e_service_icon = fields.Binary(string="Icon")
    e_service_description = fields.Html(string="Description")
    teaser = fields.Text('Teaser', compute='_compute_teaser')

    @api.depends('e_service_description')
    def _compute_teaser(self):
        for e_service in self:
            if e_service.e_service_description:
                content = html2plaintext(e_service.e_service_description).replace('\n', ' ')
                e_service.teaser = content[:200] + '...'
            else:
                e_service.teaser = False


class ProjectEServiceCategory(models.Model):
    _name = 'project.e_service.category'
    _rec_name = 'e_service_id'

    e_service_id = fields.Many2one('e_service.category', string="E-Service", required=True)
    e_service_category_icon = fields.Binary(string="Icon")
    sequence = fields.Integer(string="Sequence")
    project_id = fields.Many2one('project.project', string="Project")


class EServiceCategory(models.Model):
    _name = 'e_service.category'

    name = fields.Char(string="Name", required=True)
