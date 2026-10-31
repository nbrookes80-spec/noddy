# NSW & Australian WHS law sources

Check sources in this order. The official version wins if sources conflict.

## Legislation

| Source | What it's for | Where |
|---|---|---|
| **NSW Legislation** (Parliamentary Counsel's Office) | Official, authorised text of NSW Acts and Regulations; in-force dates; historical versions; repealed instruments | https://legislation.nsw.gov.au — search "Work Health and Safety" |
| **AustLII** — NSW Consolidated Acts | Full-text search, point-in-time notes, cross-links | https://www.austlii.edu.au/au/legis/nsw/consol_act/ (OLEXI code `au/legis/nsw/consol_act`) |
| **AustLII** — NSW Consolidated Regulations | WHS Regulation text | https://www.austlii.edu.au/au/legis/nsw/consol_reg/ |
| **AustLII** — NSW Numbered Acts / Bills | Amending Acts (e.g. industrial manslaughter, penalty increases) and their commencement | https://www.austlii.edu.au/au/legis/nsw/num_act/ · https://www.austlii.edu.au/au/legis/nsw/bill/ |
| **Federal Register of Legislation** | *WHS Act 2011* (Cth), *Fair Work Act 2009* (Cth), *Sex Discrimination Act 1984* (Cth) | https://www.legislation.gov.au |
| **Safe Work Australia** | Model WHS Act, model Regulations, model codes; national comparison tables; review reports | https://www.safeworkaustralia.gov.au/law-and-regulation |
| Other States | Qld (legislation.qld.gov.au), SA (legislation.sa.gov.au), Tas (legislation.tas.gov.au), ACT (legislation.act.gov.au), NT (legislation.nt.gov.au), WA (legislation.wa.gov.au), Vic OHS (legislation.vic.gov.au) | — |

## Case law

| Source | Coverage | Where |
|---|---|---|
| **NSW Caselaw** | Official NSW judgments: Local Court (NSWLC), District Court (NSWDC), Supreme Court (NSWSC), Court of Criminal Appeal (NSWCCA), Court of Appeal (NSWCA), Industrial Relations Commission (NSWIRComm), Industrial Court (NSWIC), NCAT, Personal Injury Commission | https://www.caselaw.nsw.gov.au |
| **AustLII** — all NSW cases | Cross-database search; older IRC WHS/OHS prosecutions | https://www.austlii.edu.au/au/cases/nsw/ (OLEXI codes `au/cases/nsw`, `au/cases/nsw/NSWDC`, `au/cases/nsw/NSWCCA`, `au/cases/nsw/NSWSC`, `au/cases/nsw/NSWCA`) |
| **AustLII** — Commonwealth | Fair Work Commission (`au/cases/cth/FWC`); Federal Court (`au/cases/cth/FCA`, `au/cases/cth/FCAFC`); High Court (`au/cases/cth/HCA`) | https://www.austlii.edu.au/au/cases/cth/ |
| **Jade** | Citator ("cited by"), clean judgment text, alerts | https://jade.io |
| **Personal Injury Commission** | Workers compensation and motor accident decisions | https://pi.nsw.gov.au (decisions are also on NSW Caselaw / AustLII) |

Key High Court authorities to look up and verify before relying on them: *Kirk v Industrial Court (NSW)* (2010) 239 CLR 531 (the particulars of the charge must identify the measures not taken; jurisdictional error); *Baiada Poultry Pty Ltd v The Queen* (2012) 246 CLR 92 (what "reasonably practicable" requires). Find later NSW WHS sentencing cases by searching NSW Caselaw for "Work Health and Safety Act 2011" together with the section, e.g. `"s 32"` or `"Category 2"`.

## Regulator guidance (not law, but relevant evidence)

| Source | What | Where |
|---|---|---|
| **SafeWork NSW** | Approved codes of practice (s 274), incident notification, enforcement and prosecution policies, published prosecution outcomes, enforceable undertakings register | https://www.safework.nsw.gov.au — notify incidents on 13 10 50 or online |
| **Safe Work Australia** | Model codes; guidance on psychosocial hazards, sexual harassment, the "reasonably practicable" test and officer due diligence | https://www.safeworkaustralia.gov.au |
| **State Insurance Regulatory Authority (SIRA)** / **icare** | Workers compensation obligations and injury notification | https://www.sira.nsw.gov.au · https://www.icare.nsw.gov.au |
| **Australian Human Rights Commission** | Positive-duty guidelines (Sex Discrimination Act s 47C) | https://humanrights.gov.au |

## AustLII search patterns

- Browse an Act: open `https://www.austlii.edu.au/au/legis/nsw/consol_act/` and pick the WHS Act from the alphabetical index. A section URL is `.../<act-slug>/s19.html`.
- Full-text search: `https://www.austlii.edu.au/cgi-bin/sinosrch.cgi?query=<terms>&meta=/au&mask_path=<db-code>` — or use the OLEXI `build_search_url` tool, which generates the same URL.
- Useful queries:
  - `"Work Health and Safety Act 2011" AND "industrial manslaughter"` in `au/legis/nsw/consol_act`
  - `"Work Health and Safety Act 2011" AND sentence AND "s 32"` in `au/cases/nsw/NSWDC`
  - `psychosocial AND "Work Health and Safety Regulation"` in `au/cases/nsw`
  - `"stop bullying" OR "stop sexual harassment"` in `au/cases/cth/FWC`

## When sources are unreachable

If a fetch or connector returns 403, a timeout or no results, say which source failed and give the user the URL to check themselves. Mark any provision you couldn't verify as **unverified**. In a Claude Code cloud session, add these hosts to the environment's allowed domains: `legislation.nsw.gov.au`, `www.austlii.edu.au`, `www.caselaw.nsw.gov.au`, `www.safework.nsw.gov.au`, `www.safeworkaustralia.gov.au`, `www.legislation.gov.au`, `jade.io`.
