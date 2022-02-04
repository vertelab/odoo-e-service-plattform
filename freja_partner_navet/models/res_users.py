import json
import logging
import requests
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.exceptions import AccessDenied, UserError

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AuthProvider(models.Model):
    _inherit = 'auth.oauth.provider'

    client_secret = fields.Char("Client Secret")

class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def create(self, vals):
        res = super(ResUsers, self).create(vals)
        source = self.env['auth.oauth.provider'].browse(vals.get('oauth_provider_id', False)).name
        if source == 'Freja eID':
            navet = self.env.ref('partner_navet.navet_interface')
            person_data = navet.navet_send_request('194107086995', 162021004748, "00000236-FO01-0001")
            res.partner_id.write({
                'street': person_data[0]['Personpost']['Adresser']['Folkbokforingsadress']['Utdelningsadress1'] or person_data[0]['Personpost']['Adresser']['Folkbokforingsadress']['Utdelningsadress2'] or False,
                'zip': person_data[0]['Personpost']['Adresser']['Folkbokforingsadress']['PostNr'] or False,
                # 'name': person_data[0]['Personpost']['Namn']['Aviseringsnamn'] or False,
            })
        return res
[{
    'Sekretessmarkering': None,
    'SkyddadFolkbokforing': None,
    'Arendeuppgift': {
        'PostId': None,
        'Arendetyp': None,
        'andringstidpunkt': 20061127104834,
        'totalpost': None,
        'utsokningsdatum': None
    },
    'Personpost': {
        'PersonId': {
            'PersonNr': 194107086995,
            'TilldelatPersonNrSamordningsNr': None,
            'Identitetsstatus': None
        },
        'HanvisningsPersonNr': None,
        'Hanvisningar': None,
        'Avregistrering': None,
        'Fodelsedatum': 19410708,
        'Namn': {
            'Tilltalsnamnsmarkering': 12,
            'Fornamn': 'Svante Hans-Emil',
            'Mellannamn': 'Andersson',
            'Efternamn': 'Grundberg',
            'Aviseringsnamn': 'Andersson Grundberg, Svante Hans E'
        },
        'Folkbokforing': {
            'Folkbokforingsdatum': 19410708,
            'LanKod': '01',
            'KommunKod': '25',
            'ForsamlingKod': None,
            'Fastighetsbeteckning': 'LÅNGA 3',
            'Trappuppgang': None,
            'Lagenhet': None,
            'FiktivtNr': 0,
            'Folkbokforingstyp': None
        },
        'Adresser': {
            'Folkbokforingsadress': {
                'CareOf': None,
                'Utdelningsadress1': None,
                'Utdelningsadress2': 'PENSÉVÄGEN 2',
                'PostNr': 17838,
                'Postort': 'EKERÖ'
            },
            'Riksnycklar': None,
            'UUID': {
                'Fastighet': '8111c620-57f3-ee5a-e053-1c80ad0a1b4b',
                'Adress': '529316c0-70cb-43d2-96d8-b61c53d265cd',
                'Lagenhet': '74f1176e-ff34-4f1f-a50b-3f2fe0d102b6'
            },
            'Distrikt': {
                'Distriktskod': 101233
            },
            'SarskildPostadress': None,
            'Utlandsadress': None
        },
        'Civilstand': {
            'CivilstandKod': 'OG',
            'Civilstandsdatum': None
        },
        'Fodelse': {
            'HemortSverige': {
                'FodelselanKod': '01',
                'Fodelseforsamling': 'BOO'
            },
            'OrtUtlandet': None
        },
        'Invandring': None,
        'Relationer': None,
        'Medborgarskap': [
            {
                'MedborgarskapslandKod': 'SE',
                'Medborgarskapsdatum': 0,
                'status': None
            }
        ],
        'Samordningsnummeruppgifter': None
    },
    'Historik': {
        'Folkbokforing': [
            {
                'Folkbokforingsdatum': 19410708,
                'LanKod': '01',
                'KommunKod': '25',
                'ForsamlingKod': None,
                'Fastighetsbeteckning': 'LÅNGA 3',
                'Trappuppgang': None,
                'Lagenhet': None,
                'FiktivtNr': None,
                'Folkbokforingstyp': 'FB'
            }
        ],
        'Folkbokforingsadress': None
    },
    'Sarlosning': None
}]