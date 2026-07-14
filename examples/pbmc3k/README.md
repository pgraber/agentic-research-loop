# Worked example — the loop on 10x PBMC 3k

A small, public dataset (10x Genomics PBMC 3k) run through the research loop, so you can see the
workflow the skills enforce without any private data. It is deliberately a *simple* analysis — the
point is the **process and the record**, not the biology.

> This mirrors how the real system works, rendered here as plain markdown. In a live project the
> checkpoints are one self-contained `docs/checkpoints.html` (visual, toggleable), and the write-up
> is a Quarto notebook rendered two ways (learning + report).

## The loop, applied

| Step | What happened here | Artifact |
|---|---|---|
| **0 Scope** | One question: *what cell populations are in PBMC 3k, and are standard QC cutoffs defensible?* | [`docs/brief.md`](docs/brief.md) |
| **1 Ground** | Standard scRNA-seq QC + clustering (Seurat); cutoffs from the field, not invented | [`docs/brief.md`](docs/brief.md) |
| **2 Intake-QC** ★ | Confirm the matrix loads, expected ~2,700 cells × ~32k genes, no empty barcodes | logged in the script |
| **3 Design** | **Pre-registered** thresholds *before* running: `nFeature 200–2500`, `percent.mt < 5%`, 10 PCs, resolution 0.5 | [`docs/checkpoints.md`](docs/checkpoints.md) |
| **4 Build** | Parameterised script + a unit-tested pure QC function | [`scripts/01_qc_cluster.R`](scripts/01_qc_cluster.R), [`scripts/functions/qc_filters.R`](scripts/functions/qc_filters.R) |
| **5 Output-QC** ★ | Do results match the pre-registered expectation? cell count after filter, cluster count | [`docs/checkpoints.md`](docs/checkpoints.md) |
| **6 Bio-sense** ★ | Do the clusters carry the *expected* PBMC markers (MS4A1 B, CD3D T, CD14 mono, NKG7 NK)? | [`docs/checkpoints.md`](docs/checkpoints.md) |
| **7 Review** | Tests pass; clean re-run gives the same result (fixed seed + captured environment) | `tests/` |
| **8 Narrate** | This README + the checkpoints are the write-up; every number traces to a `results/` file | here |
| **9 Reflect** | New concept (percent.mt as a QC axis) would go to the glossary / notes | — |

## Run it

```bash
cd examples/pbmc3k
# one-time: fetch the public dataset via SeuratData (or pass --data <10x matrix dir>)
Rscript -e 'SeuratData::InstallData("pbmc3k")'
Rscript scripts/01_qc_cluster.R --outdir results
Rscript -e 'testthat::test_dir("tests/testthat")'   # the unit tests
```

Requires R with `Seurat` (v5), `SeuratData`, `optparse`, and `testthat`. In the real system this
runs inside a pinned container so the environment is captured; here it is kept dependency-light on
purpose. PBMC 3k is a standard 10x Genomics public dataset, also distributed via the `SeuratData`
package.

## What this example is showing a reviewer

- **The approach is decided and its thresholds pre-registered before the data is touched** — no
  post-hoc cutoff tuning.
- **The number-producing logic is a pure function with a unit test** — the deterministic core is
  verified, not trusted.
- **The result is checked against a stated expectation** (output-QC) *and* against known biology
  (bio-sense) before it is believed.
- **Every step leaves a committed record** — the analysis is auditable end to end.
