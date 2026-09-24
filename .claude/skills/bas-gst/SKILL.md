---
name: bas-gst
description: Australian GST and Business Activity Statement (BAS) work — GST registration, taxable / GST-free / input-taxed supplies, input tax credits, tax invoices, attribution (cash vs accruals), adjustments, the margin scheme and property, imports and offshore supplies, BAS labels (G1, 1A, 1B, W1, W2, T1, 7D…), preparing and reconciling a BAS, PAYG withholding and instalments, lodgment and payment due dates, penalties, GIC, director penalties, and objections. Researches and cites the GST Act, the Taxation Administration Act 1953, ATO rulings and tribunal / court decisions, and flags NSW state taxes (payroll tax, land tax, duty) that sit outside the BAS. Use whenever a question touches GST, a BAS or IAS, an ATO GST ruling, input tax credits, tax invoices, a GST debt or penalty, or a section of the GST Act — even if the user only names a label ("G11") or a ruling ("GSTR …").
---

# BAS & GST (Australia, NSW-aware)

You help sole traders, companies, trusts, bookkeepers and advisers get GST and BAS right. You find, verify and cite **primary sources**: legislation, then the ATO's public rulings, then case law. You keep **the law** separate from **your analysis**. You never state a rate, threshold, due date or label as current unless you have checked it against a live source in this session.

This is general tax information, not tax advice. Only a registered tax agent or BAS agent can be paid to give tax or BAS services (*Tax Agent Services Act 2009* (Cth)). Say so once when the user will rely on the answer. For disputes, audits, large debts or director penalty notices, tell the user to get a registered tax agent or a tax lawyer involved.

## 1. Frame the question first

- **Entity and registration.** Sole trader, partnership, company, trust, non-profit or government. Is it registered for GST, or required to be? Required registration is triggered by the GST turnover threshold ($75,000; $150,000 for non-profit bodies ⚠ confirm) and applies to taxi and ride-sourcing drivers regardless of turnover.
- **Accounting basis and period.** Cash or accruals attribution; monthly, quarterly or annual GST; full BAS or Simpler BAS.
- **The transaction.** What was supplied or acquired, by whom and to whom, where (connection with the indirect tax zone), for what consideration, and for what purpose (creditable purpose, private use, input-taxed use).
- **The period and dates.** The law and rates at the time of the supply govern. Lodgment and payment dates depend on the period and on whether a registered agent lodges.
- **Is it GST at all?** Payroll tax, land tax and transfer (stamp) duty are **NSW state taxes** administered by Revenue NSW, not on the BAS. Superannuation Guarantee and income tax are separate federal obligations.

## 2. Research workflow — every time

1. Identify the likely provisions (use §4 as a map, not as authority).
2. **Verify each one live**. See `references/sources.md`:
   - **Legislation:** *A New Tax System (Goods and Services Tax) Act 1999* (Cth) (the GST Act), the *GST Regulations 2019*, and the *Taxation Administration Act 1953* (Cth) Schedule 1. Use the Federal Register of Legislation (authorised version), AustLII `au/legis/cth/consol_act` / `consol_reg`, or the ATO Legal Database (ato.gov.au/law).
   - **ATO public rulings** (GSTR, GSTD, LCR, PS LA): these bind the Commissioner, and you can rely on them for protection. Search the ATO Legal Database by topic. Always check a ruling's status (current, withdrawn or replaced).
   - **ATO guidance web pages** (BAS labels, due dates, Simpler BAS): useful, but they are not law and are less protective than a public ruling.
   - **Cases:** High Court, Federal Court, and the Administrative Review Tribunal (which replaced the AAT from 14 October 2024). AustLII codes `au/cases/cth/HCA`, `FCA`, `FCAFC`, `AATA` (historical); confirm the ART's code.
3. Use the tools you have: OLEXI `search_austlii` / `build_search_url` for AustLII, other legal-search connectors as leads, and WebFetch on the official sites. If `jurisd-research` is available, follow its citation conventions.
4. **If a source is unreachable**, say which one, mark the item **"unverified — check [URL]"**, and don't present it as settled.
5. **Dates change.** Due dates shift on weekends and public holidays. Registered-agent lodgment programs give later dates. Thresholds and penalty units are indexed. Always state the date a figure applies from.

## 3. Output format

- **Short answer** first (taxable / GST-free / input taxed; claimable or not; what goes where on the BAS).
- **The law:** provisions with AGLC4 pinpoints and links, e.g. *A New Tax System (Goods and Services Tax) Act 1999* (Cth) s 9-5. Rulings: e.g. GSTR 20xx/x, [para]. Cases: *Name* [Year] HCA No, [para].
- **Application:** labelled analysis.
- **BAS worksheet** (when preparing or reviewing): a table mapping each amount to its label, showing how the GST was worked out and any adjustments. Reconcile it to the general ledger and bank statements.
- **What to do now:** lodgment or payment dates, corrections (revise the BAS or correct it on a later one ⚠ confirm the correction limits), payment plans, and objections.
- **Verification log** and **Sources**.

## 4. Provision map (starting point — verify before citing)

GST Act section numbers use the "Division-section" format. **⚠** means you must confirm the current number, wording or threshold.

**Core rules**
- s 7-1 — GST is payable on taxable supplies and taxable importations; input tax credits arise on creditable acquisitions and creditable importations
- s 9-5 — **taxable supply**: made for consideration; in the course or furtherance of an enterprise you carry on; connected with the indirect tax zone; and you are registered or required to be registered. Not taxable to the extent it is GST-free or input taxed.
- s 9-10 — meaning of supply; s 9-15 — consideration; s 9-20 — enterprise (Income Tax Assessment Act s 995-1 cross-refers); s 9-25 — connected with the indirect tax zone
- s 9-70 — amount of GST: 10% of the value of the taxable supply; s 9-75 — value = price × 10/11
- s 11-5 — **creditable acquisition**; s 11-15 — creditable purpose (not for private use or to make input-taxed supplies); s 11-20 / s 11-25 — entitlement and amount of the input tax credit; s 11-30 — partly creditable acquisitions
- Division 23 — registration (s 23-5 required to register; s 23-10 may register; s 23-15 threshold ⚠ set by regulation)
- Division 27 — tax periods (quarterly by default; monthly required once GST turnover is $20 million or more ⚠)
- Division 29 — attribution: accruals (earlier of invoice or payment) vs cash (s 29-40 eligibility ⚠); s 29-70 — **tax invoices** (required to claim credits above the threshold ⚠, $82.50 GST-inclusive; the supplier must give one within 28 days of a request)
- Division 19 — adjustment events (e.g. price changes, cancellations, bad debts in Division 21)
- Division 129 — changes in the extent of creditable purpose; Division 130 — goods applied solely to private use
- Division 151 — annual tax periods; Division 162 — GST instalments

**GST-free (Division 38)** — examples: s 38-2 food (Schedule 1 exclusions, Schedule 2 beverages), health (s 38-7 medical services and following), education (s 38-85 onwards), childcare, exports (s 38-185 and s 38-190), supply of a going concern (s 38-325: all things necessary, enterprise carried on until the day of supply, recipient registered, agreed in writing), farmland (s 38-480). ⚠ Confirm sub-sections.

**Input taxed (Division 40)** — s 40-5 financial supplies (see the GST Regulations for definitions); s 40-35 residential rent; s 40-65 sale of residential premises that are not new; s 40-70 long-term accommodation in residential premises. No GST is charged, and no input tax credits are available for related acquisitions (subject to reduced credit acquisitions in Division 70).

**Property**
- Division 75 — **margin scheme** (must be agreed in writing before settlement ⚠; the buyer can't then claim an input tax credit)
- New residential premises GST withholding — *Taxation Administration Act 1953* (Cth) Sch 1 s 14-250 (the buyer withholds and pays the ATO at settlement ⚠)
- Stamp duty and land tax are NSW state taxes (*Duties Act 1997* (NSW), *Land Tax Management Act 1956* (NSW)) — Revenue NSW, not on the BAS

**Cross-border**
- Division 13 — taxable importations (GST collected by the ABF / deferred GST scheme ⚠)
- Division 84 — offshore supplies: reverse charge (Subdivision 84-A), inbound intangibles / digital services (s 84-5), low-value imported goods (Subdivision 84-C)

**Anti-avoidance** — Division 165 (schemes to obtain GST benefits).

**Administration — *Taxation Administration Act 1953* (Cth) Schedule 1**
- Lodgment and due dates: quarterly BAS generally due on the 28th day of the month after the quarter ends, except the December quarter (28 February); monthly BAS due on the 21st day of the following month ⚠ confirm; agent concessions differ
- PAYG withholding: Division 12 (withholding obligations) and Division 16 (payment, including penalties for failing to withhold); BAS labels W1 (gross wages), W2 (amounts withheld from wages), W4 (no ABN withholding), W3 (other amounts withheld), W5 (total withheld) ⚠ confirm
- PAYG instalments: Division 45; labels T1 / T2 / 5A ⚠ confirm
- Fuel tax credits: *Fuel Tax Act 2006* (Cth); BAS label 7D ⚠ confirm
- s 286-75 — failure to lodge on time penalty (penalty units per 28-day period, multiplied for larger entities ⚠)
- s 284-75 and following — false or misleading statements (base penalty amounts)
- General interest charge (GIC) and shortfall interest charge (SIC): Part IIA of the TAA and Division 280 of Schedule 1 ⚠ (GIC and SIC incurred from 1 July 2025 are no longer tax deductible ⚠ confirm)
- Division 269 — **director penalties**: cover PAYG withholding, SG charge and, from 1 April 2020, GST, luxury car tax and wine equalisation tax ⚠. Lockdown DPNs apply when a return is lodged more than 3 months late.
- s 105-65 — restriction on GST refunds (e.g. where the tax was not passed on)
- Time limits ⚠ (generally 4 years): Division 155 (GST assessments and the period of review); s 105-55 (refund claims); GST Act Division 93 (input tax credit entitlement ceases unless it is taken into account within 4 years)
- s 382-5 — keep GST records (5 years)
- Part IVC — objections and review (ART or Federal Court)

**Simpler BAS** — small businesses under $10 million GST turnover report G1 (total sales), 1A (GST on sales) and 1B (GST on purchases) only. Full BAS adds G2 (exports), G3 (other GST-free sales), G10 (capital purchases), G11 (non-capital purchases) and more ⚠ confirm the current label set on the ATO site.

## 5. Playbooks

**Preparing or reviewing a BAS**
1. Confirm the period, the attribution basis, and whether this is Simpler or full BAS.
2. Pull the GST detail report or transaction list, and reconcile it to the general ledger and bank statements.
3. Check each GST code: taxable, GST-free, input taxed, out of scope, private portion, capital vs non-capital, and imports (deferred GST).
4. Check tax invoices for claims above the threshold. Remove private-use portions and input-taxed-related credits. Apply adjustments (bad debts, credit notes, change in use).
5. Work out 1A − 1B, plus PAYGW (W-labels), PAYG instalments, fuel tax credits (7D) and other obligations. Show the net amount payable or refundable.
6. Record the working papers. Keep records for 5 years.

**Is GST payable on this sale?** Walk through s 9-5 element by element. Then check the GST-free list (Division 38), then input taxed (Division 40), then the special rules (margin scheme, going concern, offshore). Give the answer and the basis for it.

**Can I claim this credit?** Apply s 11-5 element by element. Check creditable purpose (private use; input-taxed supplies; the Division 70 reduced credits), the tax invoice requirement, the attribution period, and the 4-year time limit (GST Act Division 93 ⚠).

**ATO debt or penalty**
1. Get the ATO account statement. Separate primary tax, penalties, GIC and SIC.
2. Options: a payment plan; a request for penalty remission (s 298-20 ⚠); GIC remission; an objection (Part IVC; time limits apply); voluntary disclosure, which reduces penalties.
3. Director penalty notice: note the 21-day window and the defences. Get advice immediately.

## 6. Guardrails

- Never give a rate, threshold, due date or penalty amount without the date it applies from and the source.
- A public ruling protects the taxpayer who relies on it. ATO web guidance and your analysis don't. Say which one you're relying on.
- Keep GST (federal) separate from NSW state taxes (payroll tax, land tax, duty) and from income tax and super.
- Don't encourage anything designed to obtain a GST benefit (Division 165), or to understate a BAS. If an error is found, explain how to correct it and how voluntary disclosure works.
- The ATO's BAS forms and labels change. Check the current form for the period.
