{
    'name': 'Freja eID Integration',
    'summary': "Identifies partners with Freja eID via Navet.",
    'description': '''
Freja eID Integration
=====================

    Identifies partners with Freja eID via Navet.

    Features:

        - UI Integration: Extends 2 view(s) in the Odoo interface.
        - Extends Odoo: Builds on auth.oauth.provider.
    ''',
    'version': '18.0.1.0.4',
    'author': 'Verified Email Europe AB',
    'maintainer': 'Verified Email Europe AB',
    'contributors': 'Hemangi Rupareliya, Verified Email Europe AB, Fredrik Arvas',
    'website': 'https://vertel.se/apps/odoo-e-service-plattform/freja_partner_navet',
    'license': 'AGPL-3',
    'category': 'Tools',
    'depends': [
        'freja_eid_integration',
        'partner_navet',
        'auth_oauth',  # Odoo SA
        'portal',      # Odoo SA
        'hr',
        'partner_ssn',
        #'partner_extenstion_verifiedemail', # https://github.com/VerifiedEmailEurope/ve-odoo-base/tree/14.0
        #'mail_sender_whitelisting' # https://github.com/VerifiedEmailEurope/ve-odoo-mail/tree/14.0
    ],
    'application': False,
    'installable': True,
}
