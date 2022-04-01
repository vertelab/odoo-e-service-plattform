# -*- coding: utf-8 -*-
from odoo import models, fields, api
from requests import Session
from zeep import Client
from zeep.transports import Transport
from OpenSSL import crypto
import logging
_logger = logging.getLogger(__name__)

# class Partner(models.Model):
#     _inherit = "res.partner"


class NavetImport(models.Model):
    _name = "navet.import"

    name = fields.Char(string="name")
    key = fields.Char(string="Navet Key")

    def navet_send_request(self, person_number, org_number, ordering_id):
        _logger.warning("Sending navet request" * 99)
        pkcs12 = crypto.load_pkcs12(open("/usr/share/odoo-e-service-plattform/partner_navet/navet_certificates/61960e368d4c6.p12", 'rb').read(), bytes(self.key, 'utf-8'))
        cert = crypto.dump_certificate(crypto.FILETYPE_PEM, pkcs12.get_certificate())
        key = crypto.dump_privatekey(crypto.FILETYPE_PEM, pkcs12.get_privatekey())
        with open('/usr/share/odoo-e-service-plattform/partner_navet/cert.pem', 'wb') as f:
            f.write(cert)
        with open('/usr/share/odoo-e-service-plattform/partner_navet/key.pem', 'wb') as f:
            f.write(key)
        session = Session()
        session.cert = ('/usr/share/odoo-e-service-plattform/partner_navet/cert.pem', '/usr/share/odoo-e-service-plattform/partner_navet/key.pem')

        transport = Transport(session=session)
        client = Client('https://www2.test.skatteverket.se:443/na/na_epersondata/V3/personpostXML?wsdl', transport=transport)
        print(client)
        person = client.service.getData(Bestallning = {'OrgNr': org_number, 'BestallningsId': ordering_id}, PersonId = person_number)
        _logger.warning(f"person: {person}")
        return person

class PartnerNavetImport(models.TransientModel):
    _name = "partner.navet.import"

    person_number = fields.Char(string='Social Security Number')
    # org_number = fields.Integer(string='Organisational Number', default=162021004748)
    # ordering_id = fields.Char(string='Ordering Id', default='00000236-FO01-0001')


    # def navet_send_request(self):
    #     _logger.warning("Sending navet request" * 99)
    #     pkcs12 = crypto.load_pkcs12(open("/usr/share/odoo-e-service-plattform/partner_navet/navet_certificates/61960e368d4c6.p12", 'rb').read(), b"5761213661378233")
    #     cert = crypto.dump_certificate(crypto.FILETYPE_PEM, pkcs12.get_certificate())
    #     key = crypto.dump_privatekey(crypto.FILETYPE_PEM, pkcs12.get_privatekey())
    #     with open('/usr/share/odoo-e-service-plattform/partner_navet/cert.pem', 'wb') as f:
    #         f.write(cert)
    #     with open('/usr/share/odoo-e-service-plattform/partner_navet/key.pem', 'wb') as f:
    #         f.write(key)
    #     session = Session()
    #     session.cert = ('/usr/share/odoo-e-service-plattform/partner_navet/cert.pem', '/usr/share/odoo-e-service-plattform/partner_navet/key.pem')

    #     transport = Transport(session=session)
    #     client = Client('https://www2.test.skatteverket.se:443/na/na_epersondata/V3/personpostXML?wsdl', transport=transport)
    #     print(client)
    #     person = client.service.getData(Bestallning = {'OrgNr': self.org_number, 'BestallningsId': self.ordering_id}, PersonId = self.person_number)
    #     return person
    
    def action_import_navet_person(self):
        _logger.warning("Clicky buttony" * 99)
        person = self.env.ref('partner_navet.navet_interface').navet_send_request(self.person_number, 162021004748, "00000236-FO01-0001")
        self.env["res.partner"].create({
            "name": f"{person[0]['Personpost']['Namn']['Aviseringsnamn']}" or f"{person[0]['Personpost']['Namn']['Fornamn']} {person[0]['Personpost']['Namn']['Efternamn']}" or False,
            "street": f"{person[0]['Personpost']['Adresser']['Folkbokforingsadress']['Utdelningsadress2']}" or False,
            "street2": f"{person[0]['Personpost']['Adresser']['Folkbokforingsadress']['Utdelningsadress2']}" or False,
            "street": f"{person[0]['Personpost']['Adresser']['Folkbokforingsadress']['Utdelningsadress2']}" or False,
            "zip": f"{person[0]['Personpost']['Adresser']['Folkbokforingsadress']['PostNr']}" or False,
            "city": f"{person[0]['Personpost']['Adresser']['Folkbokforingsadress']['Postort']}" or False,
            "country_id": self.env["res.country"].search([('name', '=', 'Sverige')])[0].id or False,
        })
        
class ResPartner(models.Model):
    _inherit="res.partner"
    
    human_child_ids = fields.Many2many(comodel_name='res.partner', relation='human_relation_ids_rel', string='Children', column1='human_child_ids', column2='human_parent_ids')
    human_parent_ids = fields.Many2many(comodel_name='res.partner', relation='human_relation_ids_rel', string='Parents', column1='human_parent_ids', column2='human_child_ids')

    @api.model
    def getHumanRelationData(self, *args, **kwargs):
        
        
        method = kwargs.get('method')
        if method == 'children':
            children_domain = [('human_parent_ids', 'in', self.env.user.partner_id.id)]
            return self.sudo().search_read(children_domain, args)
        if method == 'partner':
            child_id = kwargs.get('child_id')
            partner_domain = [('human_child_ids', 'in', child_id), ('id', '!=', self.env.user.partner_id.id)]
            _logger.warning(f"{partner_domain=}")
            _logger.warning(f"{args=}")
            return self.sudo().search_read(partner_domain, args)
        # WIP: HAN
        # _logger.error(f"{args=}")
        # _logger.error(f"{kwargs=}")
        # elif method == 'spouse':
        #     child_id = kwargs.get('child_id')
        #     domain += [('id', '=', child_id)]
        #     _logger.error(f"{domain=}")
        #     if(child := self.sudo().search(domain)):
        #         _logger.error(f"{child=}")
        #         return child
