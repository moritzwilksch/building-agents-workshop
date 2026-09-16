# Benchmark findings: enlarged handbook vs. retrieval

Date: 2026-09-15. All numbers from runs persisted in `data/runs.sqlite3`.

## Round 3 (2026-09-15, later): BM25 retrieval backend

Second Stage 2 search backend. `HandbookBM25`
(`expense_agent/stage2/bm25.py`) indexes the same page-tagged lines with
`bm25s` and returns hits through the same context window and page tags as
the grep backend. Selected with `python -m expense_agent.stage2.run
--search bm25` (grep remains the default). No handbook or prompt change.
All runs use the wide handbook and 50 cases.

| run | pass | decision | mean err | tokens/case |
|---|---|---|---|---|
| `stage2-widehandbook` (grep) | 0.520 | 0.720 | 66 | 25.8k |
| `stage2-wideseed2` (grep) | 0.680 | 0.840 | 39 | 26.5k |
| `stage2-wideseed3` (grep) | 0.520 | 0.700 | 75 | 27.6k |
| `stage2-bm25-widehandbook` | 0.612 | 0.755 | 34 | 23.6k |
| `stage2-bm25-wideseed2` | 0.600 | 0.760 | 54 | 23.7k |
| `stage2-bm25-wideseed3` | 0.620 | 0.860 | 24 | 23.3k |

Aggregate over 3 seeds: grep pass 0.573 (sample sd 0.092), decision
0.753, 26.6k tokens/case. BM25 pass 0.611 (sample sd 0.010), decision
0.792, 23.5k tokens/case. Pooled over seeds: grep 86/150, BM25 91/149.

Findings:

- **BM25 is modestly better and far more stable.** Mean pass +4 points and
  decision +4 points, with per-seed spread collapsing from 0.09 to 0.01.
  The gain is within the grep single-run spread, so treat it as a weak
  improvement, not a closed gap.
- **BM25 is cheaper.** 23.5k vs 26.6k tokens/case: better ranking returns
  the decisive passage with less repeated querying.
- **No stage-1 recovery.** BM25 stays near 0.61, still far above stage 1's
  ~80k tokens/case but not beating it; the Figure 2 and reasoning-literal
  failures are unchanged.
- **Per-case flips (grep seed1 -> BM25 seed1):** lost `case-0007, 0013,
  0033, 0050`; won `case-0009, 0019, 0020, 0025, 0029, 0034, 0038, 0041`.
  `case-0009` (event override) and `case-0041` (pre-approval
  literalism) are two known stage-2 failure modes that BM25 recovered.
- **BM25 does not respect the self-labels better than grep.** An ad-hoc
  replay of the 40-query gate against BM25 missed `dinner cap receipt
  time` and surfaced 5 unlabelled distractor rows above decisive text,
  because its context windows mix distractor tables with neighbouring
  rows. The gate in `.data-generation/check_retrieval.py` still tests only
  the grep backend.
- **One transient failure:** `stage2-bm25-widehandbook` `case-0045` hit
  `UnexpectedModelBehavior: Exceeded maximum output retries`, unrelated to
  retrieval.

## Round 2 (2026-09-15, later): per-city tables, orthogonal filler, self-labels

Data changes since round 1 below (generator:
`.data-generation/generate_handbook_schedules.py`, now also emits chapter 14
and a new chapter 22; gate: `.data-generation/check_retrieval.py`):

1. Governing tables widened: one bullet per market (~150 lodging lines,
   ~40 tip rows, same cap values as before), chapter 9 event table gained an
   "Applies" column.
2. Keyword-orthogonal filler: 320-row settlement archive (chapter 22) and
   vocabulary-purged governance clauses, enforced by a banned-term check.
3. Self-labeling: every keyword-sharing distractor row carries its
   disqualifier ("Superseded -- never payable", "Draft -- not effective",
   "Chapter N governs", "(not adopted)", "(withdrawn)").

Handbook: 101 pages, ~76k tokens. Retrieval gate: 40 canonical queries, all
decisive texts in the top 10 (Berlin cap now rank 1, was rank 10), no
unlabelled distractor above the decisive text.

| run | seeds | pass | decision | mean err | tokens/case |
|---|---|---|---|---|---|
| stage 1, old handbook | 1 | 0.680 | 0.780 | 39 | 34.5k |
| stage 1, wide handbook | 2 | 0.680, 0.640 | 0.84, 0.80 | 32, 47 | ~80k |
| stage 2, old handbook (v3) | 1 | 0.600 | 0.740 | 52 | 25.7k |
| stage 2, wide handbook | 3 | 0.520, 0.680, 0.520 | 0.70-0.84 | 39-75 | 23-50k |

Findings:

- **Volume moves cost, not accuracy.** Stage 1 ingests 2.3x the baseline
  tokens per case while holding pass rate at 0.64-0.68. The wide tables and
  archive did not confuse it further.
- **Stage 2 did not recover.** Mean pass 0.573 (sd 0.086 across 3 seeds) vs
  0.60 on the old handbook; it does not beat stage 1. Self-labeling stopped
  the filler from flooding retrieval but not the ~8-point gap.
- **Stage-2 failures are heterogeneous:** wrongful rejections
  (pre-approval literalism, e.g. case-0041), missed event overrides
  (case-0009), and per-person cap errors on Figure 2 cases (an image, so the
  cap numbers are partially irretrievable in stage 2 by design).
- **Harness caveat:** the provider-reported `total_cost` is inconsistent
  across runs with identical token counts (stage 1: $1.00 vs $0.13 for the
  same ~80k tokens/case). Trust token counts, not the cost field.

Verdict: the data lever cannot produce stage1-worse-than-stage2 on accuracy.
Volume reliably taxes the full dump (tokens, cost, latency) but gpt-5.6-luna
absorbs the confusion. The remaining stage-2 deficit traces to retrieval
opacity (Figure 2 numbers) and reasoning literalism, which are stage-3/4
teaching content, not handbook content.

## Round 1

## Question

Can the handbook be redesigned to make the full-dump agent (Stage 1) less
efficient and less accurate, without regressing the search-tool agent
(Stage 2)?

## Change under test

Appended 7 generated chapters (15–21) to the handbook, leaving chapters
01–14 byte-identical:

- reference indices (city tiers, country schedule, item keyword index, glossary)
- superseded historical schedules and 2025 draft proposals
- documentation/retention, audit findings, misconceptions, extended Q&A
- office directory
- ~500 generic governance clauses

Every distractor is explicitly subordinate (`superseded`, `draft`,
`governs`) or defers to a governing chapter, so the single source of truth
for every case is unchanged. Generator:
`.data-generation/generate_handbook_schedules.py`.

| | old | new | ratio |
|---|---|---|---|
| pages | 35 | 80 | 2.3× |
| words | 24,092 | 44,376 | 1.84× |
| chars | 120,574 | 235,494 | 1.95× |
| ~tokens | 30,143 | 58,873 | 1.95× |

## Method

- Model: `openai:gpt-5.6-luna` (default for both stages).
- Cases: all 50 in `data/`.
- Harness: `AgentRunner` (concurrency 4), deterministic grading via
  `expense_agent.eval.scoring` (decision match and reimbursement error == 0).
- Cost from provider-reported usage; tokens = input + output.
- Each run is a single sample. No repeated trials.

## Results

| run | cases | pass | decision acc | tok/case | $/case | searches/case |
|---|---|---|---|---|---|---|
| `luna-all50-1633` (stage 1, old) | 50 | 0.680 | 0.780 | 34,522 | $0.00840 | 0.0 |
| `stage1-bighandbook` (stage 1, new) | 50 | 0.640 | 0.840 | 64,823 | $0.01583 | 0.0 |
| `stage2-v2` (stage 2, old, prompt only) | 50 | 0.540 | 0.660 | 25,277 | $0.00390 | 7.4 |
| `stage2-v3` (stage 2, old, + chapter list) | 50 | 0.600 | 0.740 | 25,710 | $0.00398 | 7.6 |
| `stage2-bighandbook` (stage 2, new, v1) | 50 | 0.520 | 0.700 | 25,975 | $0.00355 | 7.8 |
| `stage2-bighandbook2` (stage 2, new, v2) | 50 | 0.520 | 0.760 | 29,974 | $0.00375 | 8.2 |

### Full-dump effect

- Cost/effective work: **+88%** ($0.00840 → $0.01583); tokens **1.88×**.
- Pass rate: **-4 points** (0.680 → 0.640).
- Decision accuracy rose 0.780 → 0.840, so the loss is in amounts, not
  status.
- Flips (old→new), stage 1: lost `case-0005, 0007, 0009, 0020, 0044`;
  won `case-0010, 0014, 0043`.

### Search-tool effect

- Cost stayed flat (~$0.0036–0.0040/case); tokens 25.7k → 30.0k.
- Pass rate: **-8 points** vs the best old-handbook run (0.600 → 0.520),
  but the gap is within single-run spread. Stage-2 runs on the old
  handbook ranged 0.540–0.600; sd ≈ 0.037, so -0.08 is ~1 sd.
- Flips (old→new), stage 2: lost `case-0001, 0007, 0010, 0021, 0024,
  0030, 0032, 0042`; won `case-0013, 0016, 0017, 0029`.

### Retrieval is intact

For representative queries the decisive text still lands in the top 10
(grep, `CONTEXT_LINES=2`, `DEFAULT_RESULTS=10`):

| query | decisive text rank |
|---|---|
| Berlin nightly room cap | 10 |
| taxi fare threshold justification | 6 |
| client entertainment per person cap | 2, 4, 6 |
| truffle policy flowchart | 1, 2, 3 |
| tip cap Germany restaurant | 3, 5 |
| peripheral IT ticket threshold | 3 |
| weekend approval flowchart | 1, 2, 3 |
| seat reservation reimbursement | 1 |
| first class rail four hours | 5, 10 |
| international flight pre-approval | 5, 9 |

## Interpretations

- **Conflicting near-duplicates hurt both agents.** The first new-handbook
  revision dropped search pass by 8 points because the search agent
  misapplied context-free summaries and conflicting rows.
- **Mitigations applied.** Item-treatment and approval tables now defer to
  governing chapters; historical/draft tables no longer name tested cities
  or Germany. This raised stage-2 decision accuracy 0.700 → 0.760 but did
  not recover pass rate (amount errors).
- **Volume alone is a weak lever.** Within a 2× size cap, extra unrelated
  text cost full dump ~1.9× tokens but only ~4 pass points.
- **The tension is structural.** Anything that makes a full read misapply
  policy (conflicting or decontextualized rules) also makes a retrieval
  agent misapply it. Only full-dump-specific degradation (volume, burial,
  cross-references) avoids transferring to search, and it is weak here.

## Caveats

- Single run per configuration; no confidence intervals.
- Stage-2 spread (0.52–0.60) is comparable to the measured regression.
- Figures were recompiled during build and are byte-identical to HEAD;
  `git status` flags them due to a pre-existing LFS-filter mismatch.
- Four cases are dated 2023; the added precedence rule keeps v4.2
  governing all claims, so labels remain valid.

## Recommendation

1. Run each configuration 2–3× to separate signal from run noise before
   judging the 8-point search gap.
2. If strict no-regression is required, drop the historical/draft numeric
   tables and keep only volume/navigation additions (indices, archive,
   governance). Full dump stays expensive; search is untouched.
3. Accept that conflicting variants cannot be both confusing and
   retrieval-safe; budget the confusion for a later multimodal stage.
