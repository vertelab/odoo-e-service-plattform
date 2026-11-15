# odoo-e-service-plattform — gren 19.0

> **Denna gren är avsiktligt tom.** Modulerna är INTE portade till Odoo 19.
> Grenen finns så att dev-miljöer (`hansolo19`) kan klona den utan att falla,
> men den påstår ingenting om att koden är portad.

## Baseline

| | |
|---|---|
| Källa | `20.0` |
| Moduler | **7** |
| Grenar i repot | `14.0`, `18.0`, `20.0`, `main` |

## Moduler

- `e-plattform-theme`
- `freja_partner_navet`
- `mail_message_type`
- `partner_navet`
- `project_e_service`
- `website_form_stages`
- `website_project_e_service`

## Blockerare

**3 externa beroenden saknas** i Odoo 19-kärnan och OCA 19.0:

| Beroende | Behövs av |
|---|---|
| `freja_eid_integration` | `freja_partner_navet` |
| `theme_common` | `e-plattform-theme` |
| `website_form` | `website_project_e_service` |

### Prioritering

Ett beroende som blockerar många moduler ger mest nytta att lösa först:

- `freja_eid_integration` — frisläpper **1** modul(er)
- `theme_common` — frisläpper **1** modul(er)
- `website_form` — frisläpper **1** modul(er)

## Nästa steg

Portering sker på `*-pfile`-maskin med versionsagnostisk kod
(`.p.py` / `.p.xml`). Se `/skill:odoo-pfiles`.
