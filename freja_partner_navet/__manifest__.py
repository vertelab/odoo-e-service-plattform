{
    'name': 'Freja eID Integration',
    'version': '14.0.1.0.4',
    'author': 'Verified Email Europe AB',
    'maintainer': 'Verified Email Europe AB',
    'contributors': 'Hemangi Rupareliya, Verified Email Europe AB, Fredrik Arvas',
    'website': 'https://verified-email.com/',
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
