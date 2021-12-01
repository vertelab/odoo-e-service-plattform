# -*- coding: utf-8 -*-
from odoo import models, fields, api
from requests import Session
from zeep import Client
from zeep.transports import Transport
from OpenSSL import crypto
import xmltodict
import logging
_logger = logging.getLogger(__name__)

# class Partner(models.Model):
#     _inherit = "res.partner"


class Partner(models.TransientModel):
    _name = "partner.navet.import"

    person_number = fields.Char(string='Social Security Number')
    
    def action_import_navet_person(self):
        _logger.warning("Clicky buttony" * 99)
        pkcs12 = crypto.load_pkcs12(open("/usr/share/odoo-e-service-plattform/partner_navet/navet_certificates/61960e368d4c6.p12", 'rb').read(), b"5761213661378233")
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
        person = client.service.getData(Bestallning = {'OrgNr': 162021004748, 'BestallningsId': '00000236-FO01-0001'}, PersonId = self.person_number)
        self.env["res.partner"].create({
            "name": f"{person[0]['Personpost']['Namn']['Aviseringsnamn']}",
            "street": f"{person[0]['Personpost']['Adresser']['Folkbokforingsadress']['Utdelningsadress2']}",
            "street2": f"{person[0]['Personpost']['Adresser']['Folkbokforingsadress']['Utdelningsadress2']}",
            "street": f"{person[0]['Personpost']['Adresser']['Folkbokforingsadress']['Utdelningsadress2']}",
            "zip": f"{person[0]['Personpost']['Adresser']['Folkbokforingsadress']['PostNr']}",
            "city": f"{person[0]['Personpost']['Adresser']['Folkbokforingsadress']['Postort']}",
            "country_id": self.env["res.country"].search([('name', '=', 'Sweden')])[0].id,
        })