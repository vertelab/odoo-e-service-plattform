# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import ast
import base64
import datetime
import dateutil
import email
import email.policy
import hashlib
import hmac
import lxml
import logging
import pytz
import re
import socket
import time
import threading

from collections import namedtuple
from email.message import EmailMessage
from email import message_from_string, policy
from lxml import etree
from werkzeug import urls
from xmlrpc import client as xmlrpclib

from odoo import _, api, exceptions, fields, models, tools, registry, SUPERUSER_ID
from odoo.exceptions import MissingError
from odoo.osv import expression

from odoo.tools import ustr
from odoo.tools.misc import clean_context, split_every

_logger = logging.getLogger(__name__)


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    def message_post_with_template(self, template_id, email_layout_xmlid=None, auto_commit=False, **kwargs):
        """ Helper method to send a mail with a template
            :param template_id : the id of the template to render to create the body of the message
            :param **kwargs : parameter to create a mail.compose.message woaerd (which inherit from mail.message)
        """
        # Get composition mode, or force it according to the number of record in self
        if not kwargs.get('composition_mode'):
            kwargs['composition_mode'] = 'comment' if len(self.ids) == 1 else 'mass_mail'
        if not kwargs.get('message_type'):
            kwargs['message_type'] = 'comment'
            kwargs['subtype_id'] = self.env.ref('mail.mt_comment').id
        res_id = kwargs.get('res_id', self.ids and self.ids[0] or 0)
        res_ids = kwargs.get('res_id') and [kwargs['res_id']] or self.ids

        # Create the composer
        composer = self.env['mail.compose.message'].with_context(
            active_id=res_id,
            active_ids=res_ids,
            active_model=kwargs.get('model', self._name),
            default_composition_mode=kwargs['composition_mode'],
            default_model=kwargs.get('model', self._name),
            default_res_id=res_id,
            default_template_id=template_id,
            custom_layout=email_layout_xmlid,
        ).create(kwargs)
        # Simulate the onchange (like trigger in form the view) only
        # when having a template in single-email mode
        if template_id:
            update_values = composer.onchange_template_id(template_id, kwargs['composition_mode'], self._name, res_id)['value']
            composer.write(update_values)
        return composer.send_mail(auto_commit=auto_commit)