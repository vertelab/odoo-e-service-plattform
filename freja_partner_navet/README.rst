README
======

This module allows to login with Freja eID.

The module is maintained from this repo:
https://github.com/VerifiedEmailEurope/ve-odoo-auth/tree/14.0

Download
--------

This python module is hosted on github repository branch. Can be downloaded by running this command:
git clone https://github.com/VerifiedEmailEurope/ve-odoo-auth -b 14.0

Version History
---------------
1. v14.0.1.0.1 - Added module to allow user to login with Freja eID.Added SSN and country inside user when
new user sign or login from Freja eID. Also added SSN on user portal.Added source 'Freja eID' if user created from
Freja eID.

2. v14.0.1.0.3 - Added mail template to send user confirmation email on Freja eId registration.

3. v14.0.1.0.4 - Set auto delete false for mail template.


Configuration
-------------

Here are steps to configure Freja eId for test and production.

1. Install Freja eId integration module.

2. Need to create a record like following inside Setting >> Users & Companies >> Oauth Providers.

Test:
______

Name: FrejaeID Test

Client ID: cliente id of test

Client secret: client secret of test

Redirect URI for user login: domain like 'https://test.verified-email.com/web'

Allow OAuth2 password grant: Checked

Provider name: Freja eID

Body: Login with OpenID

Authentication URL: https://oidc-ct.test.frejaeid.com/oidc/authorize

Scope: openid profile email https://frejaeid.com/oidc/scopes/personalIdentityNumber

Validation URL: https://oidc-ct.test.frejaeid.com/oidc/token

Data URL: https://oidc-ct.test.frejaeid.com/oidc/userinfo



Production:
____________

Name: FrejaeID

Client ID: client id of prod

Client secret: client secret of prod

Redirect URI for user login: domain like 'https://www.verified-email.com/web'

Allow OAuth2 password grant: Checked

Provider name: Freja eID

Body: Login with OpenID

Authentication URL: https://oidc.prod.frejaeid.com/oidc/authorize

Scope: openid profile email https://frejaeid.com/oidc/scopes/personalIdentityNumber

Validation URL: https://oidc.prod.frejaeid.com/oidc/token

Data URL: https://oidc.prod.frejaeid.com/oidc/userinfo

