# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.tools.translate import html_translate
from odoo.tools import html2plaintext

import logging
_logger = logging.getLogger(__name__)


class Project(models.Model):
    _inherit = 'project.project'

    e_service_category = fields.One2many(
        comodel_name='project.e_service.category',
        inverse_name='project_id',
        string='Service Category'
    )
    e_service_description = fields.Html(string='Description')
    e_service_form = fields.Html(
        sanitize_attributes=False,
        sanitize_form=False,
        translate=html_translate,
    )
    e_service_icon = fields.Binary(string='Icon')
    is_e_service = fields.Boolean(string='Is e-service')
    require_login = fields.Boolean()
    teaser = fields.Text('Teaser', compute='_compute_teaser')

    @api.depends('e_service_description')
    def _compute_teaser(self):
        for e_service in self:
            if (content := e_service.e_service_description):
                content = html2plaintext(content).replace('\n', ' ')
                e_service.teaser = content[:200] + '...'
            else:
                e_service.teaser = False


class ProjectEServiceCategory(models.Model):
    _name = 'project.e_service.category'
    _rec_name = 'e_service_id'

    e_service_category_icon = fields.Binary(string='Icon')
    e_service_id = fields.Many2one(
        comodel_name='e_service.category',
        required=True,
        string='E-Service',
    )
    name = fields.Char(
        related='e_service_id.name',
        string='E-Service',
    )
    project_id = fields.Many2one(
        comodel_name='project.project',
        string='Project',
    )
    sequence = fields.Integer()


class EServiceCategory(models.Model):
    _name = 'e_service.category'

    name = fields.Char(required=True)
    
    
class ProjectTask(models.Model):
    _inherit = 'project.task'

    def secondary_sign(self):
        _logger.warning('---------> Secondary Sign %s' % self)
        for task in self:
            secondary = None
            for partner in task.partner_id.human_parent_ids:
                if not partner.id == task.partner_id.id:
                    secondary = partner
            _logger.warning('---------> Secondary Sign Partner %s' % secondary)
            if secondary:
                template_id = self.env['ir.model.data'].get_object_reference(
                    'project_e_service',
                    'email_template_secondary_sign')[1]
                _logger.warning('---------> Secondary Sign Template %s' % template_id)
                if template_id:
                    template = self.env['mail.template'].browse(template_id)
                    values = template.generate_email(task.id, ['subject', 'body_html', 'email_from', 'email_to', 'partner_to', 'email_cc', 'reply_to', 'scheduled_date'])
                    values['email_to'] = secondary.email
                    _logger.warning('---------> Secondary Sign Values %s' % values)
                    msg_id = self.env['mail.mail'].create(values)
                    _logger.warning('---------> Secondary Sign Msg_id %s' % msg_id)
                    if msg_id:
                        msg_id._send()
        return True
                