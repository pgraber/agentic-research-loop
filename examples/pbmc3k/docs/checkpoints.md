# Checkpoints — PBMC 3k (worked example)

*In a real project this is one self-contained, visual `docs/checkpoints.html` (sticky-sidebar TOC,
plain/technical toggle). Rendered here as markdown to keep the example dependency-light.*

---

## Design ★ — pre-registered *before* running (the anti-gaming step)

These thresholds and expectations are fixed here, ahead of touching the data, so a disappointing
result cannot quietly move a cutoff afterwards.

| Parameter | Value | Why |
|---|---|---|
| `min_features` | 200 | drop empty / low-quality droplets |
| `max_features` | 2500 | drop likely doublets |
| `max_percent_mt` | 5% | drop dying/stressed cells |
| PCs | 10 | PBMC 3k signal is captured in the first ~10 PCs (tutorial standard) |
| resolution | 0.5 | expected to yield ~8–9 clusters |
| seed | 42 | deterministic re-run |

**Pre-registered expectations (what "success" looks like):**
- ~2,600–2,700 cells survive QC (from ~2,700 loaded).
- 8–9 clusters at resolution 0.5.
- Every canonical PBMC lineage marker is enriched in at least one cluster.

---

## Output-QC ★ — do the numbers match the pre-registration?

Checked against `results/qc_summary.csv` (every number traces to that file, never to a chat):

- [ ] `n_cells_pass` within the pre-registered 2,600–2,700 band
- [ ] `n_clusters` in 8–9
- [ ] `median_percent_mt` well under the 5% ceiling (sanity that the filter did its job)

*If a number falls outside the band, the loop fails backward to design — it does not proceed to
interpretation.*

---

## Bio-sense ★ — is it biologically plausible?

Checked against `results/marker_avg_expression.csv` — the canonical PBMC markers must localise to
sensible clusters:

| Marker | Lineage | Expectation |
|---|---|---|
| `CD3D` | T cells | high in the largest cluster(s) |
| `MS4A1` | B cells | one distinct cluster |
| `CD14` | Monocytes | one distinct cluster |
| `FCGR3A` | FCGR3A+ monocytes | a smaller monocyte cluster |
| `NKG7` | NK cells | one cluster, distinct from T |
| `PPBP` | Platelets | a small, very distinct cluster |

The scientific call is the human's: markers landing where PBMC biology predicts = the analysis is
believable; markers scattered or absent = stop and investigate before believing anything.
