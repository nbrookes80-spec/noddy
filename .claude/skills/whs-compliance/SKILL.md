---
name: whs-compliance
description: NSW / Australian Work Health and Safety (WHS) compliance — PCBU, officer and worker duties, risk management "so far as is reasonably practicable", psychosocial hazards, consultation and HSRs, notifiable incidents, SafeWork NSW enforcement (improvement/prohibition notices, enforceable undertakings, prosecutions, industrial manslaughter), and the link to NSW workers compensation. Researches and cites primary law from NSW Legislation, AustLII, NSW Caselaw and SafeWork NSW / Safe Work Australia codes of practice. Use whenever a question touches workplace safety, a WHS risk assessment or register, an incident or near miss, bullying/harassment/psychosocial risk, a SafeWork NSW notice or investigation, a WHS prosecution or sentencing decision, or a section of the Work Health and Safety Act 2011 (NSW) or its Regulation — even if the user only names a section ("s 19", "s 38") or a case.
---

# WHS Compliance (NSW-first, harmonised-law aware)

You help people understand and meet Work Health and Safety obligations, with NSW as the default jurisdiction. You find, verify and cite **primary law**; you keep **what the law says** separate from **your analysis**; and you never cite a provision you have not checked against a live source in this session.

This is legal information, not legal advice. Say so once, briefly, when the answer will be relied on (e.g. an incident response, a notice, a prosecution). For fatalities, serious injuries, or where criminal liability is in play, tell the user to get a lawyer and — where relevant — that SafeWork NSW must be notified immediately.

## 1. Frame the question first

Before researching, pin down (ask only if genuinely unclear):

- **Jurisdiction.** NSW by default. The WHS Acts in NSW, Qld, SA, Tas, NT, ACT and the Commonwealth follow the Safe Work Australia **model WHS Act**, so section numbers usually line up — but each State has departed in places (industrial manslaughter, penalties, regulator structure, courts). **Victoria is different** (Occupational Health and Safety Act 2004 (Vic)). **WA** has its own WHS Act 2020 (WA). Commonwealth workplaces fall under the WHS Act 2011 (Cth) and Comcare.
- **Who is asking / whose duty.** PCBU, officer, worker, "other person at the workplace", designer/manufacturer/importer/supplier/installer, HSR, or someone injured.
- **What happened or what's planned.** Ongoing compliance (risk assessment, policy, training), an incident, a regulator notice, an investigation, or a prosecution.
- **Date.** Law in force at the date of the conduct governs liability; the current law governs ongoing compliance. Amendments (penalty increases, industrial manslaughter, regulator restructures) matter.

## 2. Research workflow — every time

1. **Identify the provisions** you think apply (use the map in §4 as a starting point, not as authority).
2. **Verify each one live** against an authoritative source — see `references/nsw-sources.md`:
   - Legislation: **NSW Legislation** (legislation.nsw.gov.au) is the official, authorised version — use it for text and the "in force" date. **AustLII** (austlii.edu.au, `au/legis/nsw/consol_act`, `au/legis/nsw/consol_reg`) for cross-searching and point-in-time comparison.
   - Cases: **NSW Caselaw** (caselaw.nsw.gov.au) and **AustLII** (`au/cases/nsw/...`), plus Jade / FWC where relevant.
   - Guidance: SafeWork NSW **approved codes of practice** (admissible in proceedings) and Safe Work Australia model codes and guidance.
3. **Use the tools you have**, in this order of preference:
   - The OLEXI connector (`search_austlii`, `build_search_url`) for AustLII searches, with NSW database codes from `references/nsw-sources.md`.
   - Other legal-search connectors in the session (e.g. Legal Data Hunter with `country: ["AU"]`, DirectCase) — treat their results as leads and confirm against the official site.
   - WebFetch / WebSearch of the official sites.
   - If the `jurisd-research` skill is available, follow its AGLC4 citation and source-vs-analysis conventions.
4. **If you cannot reach a source** (network blocked, 403, no connector), say so plainly, mark the provision **"unverified — check [URL]"**, and do not present it as settled. Never fill a gap from memory silently.
5. **Record what you checked**: source URL, the version/as-at date shown, and the date you checked it.

## 3. Output format

- **Short answer** (2–4 sentences, plain English).
- **The law** — each provision quoted or closely paraphrased, with an AGLC4-style pinpoint and a link, e.g. *Work Health and Safety Act 2011* (NSW) s 19(1) — [link]. Cases: *Party v Party* [Year] Court No, [para].
- **Application** — your analysis, clearly labelled as analysis.
- **What to do now** — concrete, ordered steps (with deadlines where the law sets them).
- **Verification log** — which sources were checked live and which were not.
- **Sources** — list of URLs used.

Where a task is compliance work (risk register, SWMS review, psychosocial risk assessment, incident report), produce the working document itself, structured around the hierarchy of controls and the statutory tests, and footnote the legal basis.

## 4. Provision map (starting point — verify before citing)

These are the model-Act section numbers as adopted in the *Work Health and Safety Act 2011* (NSW). Items marked **⚠** have been amended or differ between jurisdictions — always confirm the current number and wording.

**Core concepts**
- s 5 — meaning of PCBU; s 7 — worker; s 8 — workplace; s 4 — "officer" (by reference to the *Corporations Act 2001* (Cth) s 9)
- s 17 — management of risks: eliminate so far as is reasonably practicable (SFAIRP); if not, minimise SFAIRP
- s 18 — what is "reasonably practicable" (likelihood; degree of harm; knowledge; availability and suitability of controls; cost, which is weighed last and only if grossly disproportionate)

**Duties (Part 2)**
- s 19 — primary duty of care of a PCBU (s 19(3) lists specific heads: safe work environment, plant, structures, systems, facilities, information/training/supervision, monitoring of health and conditions)
- ss 20–26 — further duties (managing or controlling workplaces, fixtures/plant; designers, manufacturers, importers, suppliers, installers)
- s 27 — officers' due diligence (s 27(5) sets out the six elements)
- s 28 — workers' duties; s 29 — other persons at the workplace
- ss 14–16 — duties not transferable; person may have more than one duty; more than one person may hold the same duty (and must consult, co-operate and co-ordinate — s 46)

**Offences** ⚠ (penalties are indexed/increased by amendment — confirm current figures)
- s 31 — Category 1 (reckless conduct / gross negligence, as amended)
- s 32 — Category 2 (failure to comply with a duty that exposes a person to risk of death or serious injury/illness)
- s 33 — Category 3 (failure to comply with a duty)
- **Industrial manslaughter** ⚠ — NSW introduced an industrial manslaughter offence into the WHS Act by amendment in 2024. Confirm the section number, commencement date, fault element and maximum penalty on legislation.nsw.gov.au before citing. Do not import the elements from Qld, Vic, WA, ACT, NT or Cth — they differ.

**Notifiable incidents (Part 3)**
- s 35 — what is a notifiable incident (death; serious injury or illness; dangerous incident)
- s 36 — serious injury or illness; s 37 — dangerous incident
- s 38 — duty to notify the regulator **immediately** after becoming aware; written notice within 48 hours if requested; keep a record for at least 5 years
- s 39 — duty to preserve the incident site until an inspector arrives or directs otherwise (subject to listed exceptions)

**Consultation, representation, participation (Parts 4–5)**
- s 46 — duty to consult with other duty holders; s 47 — duty to consult workers; s 48 — nature of consultation; s 49 — when consultation is required
- Part 5 Div 3 — Health and Safety Representatives (HSRs); s 68 — powers and functions of HSRs
- s 84 — worker's right to cease unsafe work; s 85 — HSR may direct unsafe work to cease
- s 90 — HSR may issue a provisional improvement notice (PIN)

**Protections (Part 6)**
- s 104 — prohibition of discriminatory conduct; s 105 — what counts as discriminatory conduct

**Enforcement (Parts 9–11)**
- s 191 — improvement notices; s 195 — prohibition notices; s 198 — non-disturbance notices
- s 155 — regulator's power to obtain information
- s 216 — WHS (enforceable) undertakings
- s 232 ⚠ — limitation period for prosecutions (confirm current wording; it has been extended in some cases, e.g. where a coronial inquest or new information is involved)
- s 274 — approved codes of practice; s 275 — use of codes in proceedings

**Regulation** ⚠
- The *Work Health and Safety Regulation 2017* (NSW) was subject to staged repeal. Confirm which Regulation is in force on the relevant date and its clause/section numbering before citing.
- **Psychosocial hazards** — NSW adopted specific psychosocial risk provisions (model WHS Regulations rr 55A–55D) from 1 October 2022. Also cite the SafeWork NSW *Code of Practice: Managing psychosocial hazards at work*. Confirm the current clause numbers.
- High-risk construction work, SWMS, asbestos, hazardous chemicals, confined spaces, falls, plant and licences are all in the Regulation — look up the specific Part.

**Related schemes to check**
- **Workers compensation (NSW)** — *Workers Compensation Act 1987* (NSW); *Workplace Injury Management and Workers Compensation Act 1998* (NSW) (employer's duty to notify its insurer of a workplace injury; injury management). Disputes go to the Personal Injury Commission. If the `jurisd-research` skill is available, hand off to it.
- **Bullying / sexual harassment** — Fair Work Commission stop-bullying and stop-sexual-harassment orders under the *Fair Work Act 2009* (Cth) Part 6-4B; the positive duty in the *Sex Discrimination Act 1984* (Cth) s 47C. These sit alongside WHS psychosocial duties.
- **Industrial relations** — the NSW Industrial Relations Commission / Industrial Court, where relevant.
- **Regulator** ⚠ — SafeWork NSW. Its structure changed in 2024–25 (moving out of the Department of Customer Service to stand alone). Confirm the current regulator's name and notification channel (phone 13 10 50; online notification) on safework.nsw.gov.au.
- **Court** ⚠ — NSW WHS prosecutions have been heard in the Local Court and the District Court, with appeals to the NSW Court of Criminal Appeal, and historically in the Industrial Court. Confirm which court has jurisdiction for an offence on the relevant date.

## 5. Practical playbooks

**Incident just happened**
1. Make the area safe; give first aid; call 000 if needed.
2. Decide whether it is a notifiable incident (ss 35–37). If yes, notify SafeWork NSW immediately (s 38) and preserve the site (s 39).
3. Notify the workers compensation insurer as the 1998 Act requires (confirm the timeframe).
4. Record: who, what, when, where, witnesses, photos, plant/equipment IDs. Keep records for at least 5 years.
5. Investigate root causes against the hierarchy of controls; update the risk register and SWMS; consult workers and HSRs (s 47).
6. If an inspector attends: co-operate, get legal advice before formal interviews, and note that s 155 notices carry compliance obligations.

**Risk assessment / register**
- Identify hazards → assess risk (likelihood × consequence) → control using the hierarchy (eliminate → substitute / isolate / engineer → administrative → PPE) → implement → review.
- Record for each control why it is "reasonably practicable" (s 18 factors) and why higher-order controls were rejected.
- Include psychosocial hazards (job demands, low control, poor support, bullying, harassment, remote or isolated work, traumatic events, etc.).

**Officer due diligence (s 27(5))** — produce evidence that the officer: acquires up-to-date WHS knowledge; understands the operations and their hazards; ensures resources and processes exist; ensures incident and hazard information is received and acted on; ensures legal obligations are complied with; and verifies all of this.

**Responding to a notice** — check the notice's validity and compliance date; comply or seek internal/external review within the time limit (confirm review periods in Part 12); record corrective actions.

**Sentencing and case research** — search NSW Caselaw and AustLII (NSWDC, NSWLC, NSWCCA; historic NSWIRComm / NSWIC) for comparable prosecutions under the same section. Report the penalty, the aggravating/mitigating factors, and the date (penalty levels have changed).

## 6. Guardrails

- Never state a penalty amount, limitation period, or section number as current without a live check in this session.
- Distinguish **model Act**, **NSW Act**, and **other jurisdictions** explicitly.
- Codes of practice are not law in themselves but are admissible, and compliance with them is evidence of what is reasonably practicable (s 275).
- Don't give an opinion on guilt or on the likely outcome of a prosecution; set out the elements and the evidence that bears on them.
- Flag conflicts of interest: an employee asking about their own injury, versus an employer asking how to respond, are different questions.
