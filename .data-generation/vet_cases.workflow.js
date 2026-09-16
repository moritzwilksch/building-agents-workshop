export const meta = {
  name: "vet_invoice_cases",
  description:
    "Audit all invoice.json cases against the expense handbook, rebalance the difficulty distribution, fix consistency, and verify the results",
  phases: [
    { title: "Audit" },
    { title: "Plan" },
    { title: "Fix" },
    { title: "Verify" },
    { title: "Repair" },
  ],
};

// ---- Static inputs -------------------------------------------------------
const caseIds = [
  "case-0001","case-0002","case-0003","case-0004","case-0005","case-0006","case-0007","case-0008","case-0009","case-0010",
  "case-0011","case-0012","case-0013","case-0014","case-0015","case-0016","case-0017","case-0018","case-0019","case-0020",
  "case-0021","case-0022","case-0023","case-0024","case-0025","case-0026","case-0027","case-0028","case-0029","case-0030",
  "case-0031","case-0032","case-0033","case-0034","case-0035","case-0036","case-0037","case-0038","case-0039","case-0040",
  "case-0041","case-0042","case-0043","case-0044","case-0045","case-0046","case-0047","case-0048","case-0049","case-0050",
];

const ROOT = "/home/moritz/code/building-agents-workshop";
const HANDBOOK_DIR = `${ROOT}/.data-generation/handbook`;
const HANDBOOK_FILES = [
  "01-general-policy.typ","02-submission-deadlines.typ","03-approval-workflows.typ","04-air-travel.typ",
  "05-ground-transportation.typ","06-lodging.typ","07-meals-per-diem.typ","08-client-entertainment.typ",
  "09-weekend-holiday.typ","10-equipment-supplies.typ","11-non-reimbursable.typ","12-foreign-currency.typ",
  "13-flowcharts.typ","14-appendix-tables.typ",
];
const handbookList = HANDBOOK_FILES.map((f) => `- ${HANDBOOK_DIR}/${f}`).join("\n");

const handbookBrief = `The handbook sources are Typst files in reading order. Read ALL of them before judging a case:
${handbookList}
Also read ${HANDBOOK_DIR}/main.typ to confirm the order. The handbook contains rules that interact (e.g. truffle rule + per-diem caps, weekend flowchart + lodging caps, tip caps by country, alcohol allowance percentages, foreign-currency cap conversion). Flowcharts in 13-flowcharts.typ are authoritative for weekend and dining decisions.`;

const sharedRules = `Working directory: ${ROOT}. Case directory: ${ROOT}/data/<case_id> containing invoice.json (always) and optionally label.json and receipt.jpg.

Invoice archetypes and their fields vary (restaurant, standard, taxi, hotel, flight, train, fuel, office_supplies, card_slip). Inspect the file; do not assume a schema.

After ANY edit to invoice.json, validate arithmetic with:
  cd ${ROOT}/.data-generation && pixi run python validate_invoices.py ../data/<case_id>
It must pass with no problems. Line items must multiply out, subtotals and taxes must sum to total_amount to the cent, and the appended charges list (if present) must mirror the items.

If the case has receipt.jpg and you changed invoice.json, regenerate the image so it stays grounded:
  cd ${ROOT}/.data-generation && pixi run python generate_image.py ../data/<case_id>
If image generation fails twice, revert the invoice change instead of leaving a mismatched receipt, and report the failure.

label.json is ground truth. If you change invoice.json amounts/decisions for a case that has label.json, update label.json to match the new correct adjudication (decision, claimed_amount, reimbursed_amount, line_items with ids matching charges order, reasoning citing the rule IDs you relied on).`;

const categories = ["valid", "obvious_violation", "subtle_single", "subtle_multi"];
const categoryGuide = `Difficulty categories:
- "valid": fully reimbursable per the handbook; nothing deductible. Should still be interesting (near a threshold, plausible-looking, occasionally with a distractor item that turns out to be allowed).
- "obvious_violation": clear, easy-to-spot rule breach (e.g. truffle dish, clearly over a hard cap, personal expense on the invoice). One or two cases total across the set.
- "subtle_single": deductible amount, but you must know one specific handbook passage (percentage, exception, tip norm) to spot it.
- "subtle_multi": correct adjudication requires combining two or more handbook passages (e.g. a flowchart outcome plus a cap from the appendix, or weekend rules plus an alcohol allowance).`;

// ---- Phase 1: Audit (read-only, parallel) --------------------------------
phase("Audit");
log(`Auditing ${caseIds.length} cases against the handbook`);

const auditSchema = {
  type: "object",
  properties: {
    case_id: { type: "string" },
    invoice_type: { type: "string" },
    current_category: { type: "string", enum: categories },
    intended_rules: { type: "string", description: "Which handbook passages this case appears designed to exercise" },
    consistency_issues: { type: "array", items: { type: "string" } },
    handbook_issues: { type: "array", items: { type: "string" } },
    arithmetic_ok: { type: "boolean" },
    has_label: { type: "boolean" },
    label_correct: { type: "string", enum: ["yes", "no", "no_label", "not_checked"] },
    realism_issues: { type: "array", items: { type: "string" }, description: "Vendor/city/price realism problems, if any" },
    recommendation: { type: "string", enum: ["keep", "fix", "retarget"] },
    notes: { type: "string" },
  },
  required: ["case_id", "invoice_type", "current_category", "intended_rules", "consistency_issues", "handbook_issues", "arithmetic_ok", "has_label", "label_correct", "realism_issues", "recommendation", "notes"],
};

const audits = await parallel(
  caseIds.map((id) => () =>
    agent(
      `You are auditing one synthetic expense case for a workshop that teaches agents to adjudicate claims against a company handbook. READ-ONLY: do not modify any file.

${handbookBrief}

${sharedRules}

Audit case ${id}:
1. Read ${ROOT}/data/${id}/invoice.json (and label.json / receipt.jpg presence via ls).
2. Run the arithmetic validator (see above) and report whether it passes.
3. Judge internal consistency: vendor name/address/city/country plausible for the items bought (a Berlin restaurant serves German food, a Leipzig office supplier sells stationery, taxi pickups match the note's locations), prices realistic for the venue and city, dates sane, quantities sensible. Price oddities are acceptable ONLY when they implement an intentional handbook violation - otherwise flag them.
4. Judge handbook outcome: what would the correct decision, payout, and rule citations be? Classify the case into exactly one difficulty category (see guide below).
5. If label.json exists, check it against your adjudication: decision, amounts, line items, reasoning, rule citations.
6. Recommend: "keep" (fits target distribution and is correct), "fix" (right idea, consistency/realism/label problems), or "retarget" (should become a different category for distribution balance).

${categoryGuide}

Return the structured audit.`,
      { label: `audit:${id}`, schema: auditSchema },
    ),
  ),
);

const auditFailures = caseIds.filter((id, i) => audits[i] === null);
const okAudits = caseIds.flatMap((id, i) => (audits[i] === null ? [] : [{ id, audit: audits[i] }]));
log(`Audit done: ${okAudits.length} succeeded, ${auditFailures.length} failed`);

// ---- Phase 2: Plan (single agent balances the distribution) ---------------
phase("Plan");

const planSchema = {
  type: "object",
  properties: {
    assignments: {
      type: "array",
      items: {
        type: "object",
        properties: {
          case_id: { type: "string" },
          action: { type: "string", enum: ["keep", "edit"] },
          target_category: { type: "string", enum: categories },
          guidance: { type: "string", description: "Concrete, self-contained instructions: which rules to exercise, what to change, what to keep" },
        },
        required: ["case_id", "action", "target_category", "guidance"],
      },
    },
    distribution_summary: { type: "string" },
  },
  required: ["assignments", "distribution_summary"],
};

const plan = await agent(
  `You are balancing a benchmark's difficulty distribution. Below are audits of 50 expense cases, each classified by how hard it is to adjudicate against the handbook.

${categoryGuide}

Target distribution across all 50 cases:
- About half (~24-26) "valid" - fully reimbursable.
- About 2 "obvious_violation".
- The rest split between "subtle_single" and "subtle_multi", with "subtle_multi" getting the larger share (at least 10), spread across DIFFERENT handbook areas (meals/per-diem, alcohol, tips, lodging, weekend/flowchart, client entertainment, air travel, ground transport, foreign currency, equipment/supplies, non-reimbursable catalog). Avoid stacking many cases on the same rule.

Principles:
- Minimize churn: keep every case that already fits the target category and has no serious issues. Do not retarget a good case just to shuffle.
- Prefer "fix" over "retarget" when the case's rule area is underrepresented.
- Retarget only where the distribution demands it; give the receiving case concrete new instructions.
- Every "edit" assignment's guidance must be self-contained: name the handbook passages (section numbers/titles) to exercise, the intended outcome (approved/partially/rejected and roughly how much is deducted), and any consistency fixes needed.

Audits (JSON):
${JSON.stringify(okAudits.map(({ id, audit }) => ({ case_id: id, audit })), null, 1)}

Cases that failed audit (treat as "edit" with guidance to re-verify everything): ${JSON.stringify(auditFailures)}

Return one assignment per case id (${caseIds.join(", ")}).`,
  { label: "plan:distribution", schema: planSchema },
);

if (plan === null) {
  return { error: "Plan phase failed; no assignments produced", audits: okAudits, auditFailures };
}
const byId = new Map(plan.assignments.map((a) => [a.case_id, a]));
const assignments = caseIds.map((id) => byId.get(id) || { case_id: id, action: "keep", target_category: "valid", guidance: "No plan entry; leave unchanged." });
log(`Plan: ${assignments.filter((a) => a.action === "edit").length} cases to edit. ${plan.distribution_summary}`);

// ---- Phase 3: Fix (parallel, only edited cases) ---------------------------
phase("Fix");

const fixSchema = {
  type: "object",
  properties: {
    case_id: { type: "string" },
    changed: { type: "boolean" },
    validator_passed: { type: "boolean" },
    receipt_regenerated: { type: "string", enum: ["yes", "no", "not_needed", "failed_reverted"] },
    label_updated: { type: "string", enum: ["yes", "no", "not_needed", "failed"] },
    achieved_category: { type: "string", enum: categories },
    summary: { type: "string" },
  },
  required: ["case_id", "changed", "validator_passed", "receipt_regenerated", "label_updated", "achieved_category", "summary"],
};

const toEdit = assignments.filter((a) => a.action === "edit");
const fixes = await parallel(
  toEdit.map((a) => () =>
    agent(
      `You are improving one synthetic expense case for an agent-adjudication benchmark. Apply the plan, keep the data coherent, and leave everything else untouched.

${handbookBrief}

${sharedRules}

Case: ${ROOT}/data/${a.case_id}

Target category: ${a.target_category}
Plan guidance: ${a.guidance}

Steps:
1. Read invoice.json fully. Decide the minimal-but-sufficient edit set to (a) realize the target category and (b) fix every consistency, realism, arithmetic, and label issue you can see.
2. Apply edits with the edit tool. Preserve the archetype's field structure. Keep vendor details plausible: name, city, and country must fit the goods; tax IDs and phone numbers must keep their format; item prices must fit the venue type unless a handbook rule intentionally violates this.
3. Run the validator until it passes (see shared rules).
4. If receipt.jpg exists and the invoice changed, regenerate it (see shared rules). If generation fails twice, revert the invoice change.
5. If label.json exists, bring it in line with the new invoice per LABELING.md (${ROOT}/.data-generation/LABELING.md): recompute decision, amounts, line items, and reasoning with rule citations. If a label exists but your change keeps the correct adjudication identical, still verify and report "yes" only if you touched it.
6. Do NOT edit any other file.

Return the structured result.`,
      { label: `fix:${a.case_id}`, schema: fixSchema },
    ),
  ),
);

const fixResults = toEdit.map((a, i) => ({ case_id: a.case_id, target: a.target_category, result: fixes[i] }));
const fixFailures = fixResults.filter((r) => r.result === null).map((r) => r.case_id);
const fixSummaries = fixResults.flatMap((r) => (r.result === null ? [] : [r]));
log(`Fix done: ${fixSummaries.length} edited, ${fixFailures.length} agent failures`);

// ---- Phase 4: Verify (parallel, every case, fresh eyes) -------------------
phase("Verify");

const verifySchema = {
  type: "object",
  properties: {
    case_id: { type: "string" },
    pass: { type: "boolean" },
    category_confirmed: { type: "string", enum: categories },
    problems: { type: "array", items: { type: "string" } },
  },
  required: ["case_id", "pass", "category_confirmed", "problems"],
};

const fixNotesById = new Map(fixSummaries.map((r) => [r.case_id, r.result.summary]));
const verifyResults = await parallel(
  caseIds.map((id) => () => {
    const assignment = assignments.find((a) => a.case_id === id);
    const fixNote = fixNotesById.get(id);
    return agent(
      `You are a skeptical verifier for one synthetic expense case. Another agent may have just edited it. Do NOT modify any file; report only.

${handbookBrief}

${sharedRules}

Case: ${ROOT}/data/${id}
Planned target category: ${assignment.target_category}
${fixNote ? `Editor's claim: ${fixNote}` : "This case was not edited in the fix phase."}

Verify rigorously:
1. Run the arithmetic validator; it must pass.
2. Read invoice.json and adjudicate it independently against the handbook: correct decision, exact payout, and the rule IDs a careful auditor would cite. For "valid" cases confirm NOTHING is deductible; for violation cases confirm the deduction follows from the named passages and compute the exact reimbursable amount.
3. If label.json exists, check it matches your independent adjudication (decision, amounts, line items by id, rule citations in reasoning).
4. Check realism: vendor/city/country fit the items, prices fit the venue (except intentional violations), dates coherent with the note.
5. Confirm the case actually lands in the planned category: a "valid" case must be fully reimbursable; "subtle_multi" must genuinely need at least two distinct handbook passages; "obvious_violation" must be spotted easily.

Return the structured verdict with concrete problems (quote the numbers and rule IDs).`,
      { label: `verify:${id}`, schema: verifySchema },
    );
  }),
);

const verifyFailures = caseIds.filter((id, i) => verifyResults[i] === null);
const verdicts = caseIds.flatMap((id, i) => (verifyResults[i] === null ? [] : [{ id, verdict: verifyResults[i] }]));
const failedCases = verdicts.filter(({ verdict }) => !verdict.pass);
log(`Verify done: ${verdicts.length - failedCases.length} pass, ${failedCases.length} fail, ${verifyFailures.length} agent failures`);

// ---- Phase 5: Repair (parallel, only failed cases) ------------------------
phase("Repair");

const repairSchema = {
  type: "object",
  properties: {
    case_id: { type: "string" },
    fixed: { type: "boolean" },
    what_changed: { type: "string" },
    residual_problems: { type: "array", items: { type: "string" } },
  },
  required: ["case_id", "fixed", "what_changed", "residual_problems"],
};

let repairs = [];
if (failedCases.length > 0) {
  repairs = await parallel(
    failedCases.map(({ id, verdict }) => () =>
      agent(
        `You are repairing one synthetic expense case that failed verification. Other cases are out of scope.

${handbookBrief}

${sharedRules}

Case: ${ROOT}/data/${id}
Planned target category: ${assignments.find((a) => a.case_id === id).target_category}
Verifier's problems:
${JSON.stringify(verdict.problems, null, 1)}

Fix invoice.json (and label.json / receipt.jpg per the shared rules) so every listed problem is resolved while the case lands in the planned category. Re-run the validator. If a problem cannot be fixed without breaking the archetype schema, choose the nearest consistent alternative and report it as residual.`,
        { label: `repair:${id}`, schema: repairSchema },
      ),
    ),
  );
}

const repairResults = failedCases.map(({ id }, i) => ({ case_id: id, repair: repairs[i] }));

// ---- Final report ----------------------------------------------------------
return {
  distribution_plan: plan.distribution_summary,
  assignments: assignments.map((a) => ({ case_id: a.case_id, action: a.action, target_category: a.target_category })),
  audit_failures: auditFailures,
  fix_results: fixSummaries.map((r) => ({ case_id: r.case_id, ...r.result })),
  fix_agent_failures: fixFailures,
  verification: verdicts.map(({ id, verdict }) => ({ case_id: id, ...verdict })),
  verify_agent_failures: verifyFailures,
  repairs: repairResults.map(({ case_id, repair }) => ({ case_id, repair })),
  residual_failures: repairResults
    .filter(({ repair }) => repair === null || repair.fixed === false || (repair.residual_problems || []).length > 0)
    .map(({ case_id, repair }) => ({ case_id, repair })),
};
