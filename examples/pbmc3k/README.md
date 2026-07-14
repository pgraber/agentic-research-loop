# Worked example: the loop on 10x PBMC 3k

A small public dataset (10x Genomics PBMC 3k) run through the research loop, so you can see the
workflow the skills enforce without any private data. This is deliberately a simple analysis. The
point is the process and the record, not the biology.

> This mirrors how the real system works, shown here as plain files. In a live project the
> checkpoints are one self-contained `docs/checkpoints.html`, and the write-up is a Quarto notebook
> ([`report.qmd`](report.qmd)) rendered two ways: a learning version and a clean report.

## The loop, applied

| Step | What happened here | Artifact |
|---|---|---|
| **0 Scope** | One question: what cell populations are in PBMC 3k, and are the standard QC cutoffs defensible? | [`docs/brief.md`](docs/brief.md) |
| **1 Ground** | Standard scRNA-seq QC and clustering (Seurat), with cutoffs taken from the field rather than invented | [`docs/brief.md`](docs/brief.md) |
| **2 Intake-QC** ★ | Confirm the matrix loads, roughly 2,700 cells, no empty barcodes | logged in the script |
| **3 Design** | Thresholds pre-registered before running: nFeature 200 to 2500, percent.mt below 5, 10 PCs, resolution 0.5 | [`docs/checkpoints.md`](docs/checkpoints.md) |
| **4 Build** | Parameterised script plus a unit-tested pure QC function | [`scripts/01_qc_cluster.R`](scripts/01_qc_cluster.R), [`scripts/functions/qc_filters.R`](scripts/functions/qc_filters.R) |
| **5 Output-QC** ★ | Do the results match the pre-registered expectation (cells after filter, cluster count)? | [`docs/checkpoints.md`](docs/checkpoints.md) |
| **6 Bio-sense** ★ | Do the clusters carry the expected PBMC markers (MS4A1 for B, CD3D for T, CD14 for monocytes, NKG7 for NK)? | [`docs/checkpoints.md`](docs/checkpoints.md) |
| **7 Review** | Tests pass, and a clean re-run with a fixed seed gives the same result | `tests/` |
| **8 Narrate** | A literate Quarto report that reads from `results/`, with every number traced to a file | [`report.qmd`](report.qmd) |
| **9 Reflect** | A new concept (percent.mt as a QC axis) would go to the glossary or notes | n/a |

## Run it

```bash
cd examples/pbmc3k
# one-time: fetch the public dataset via SeuratData (or pass --data <10x matrix dir>)
Rscript -e 'SeuratData::InstallData("pbmc3k")'
Rscript scripts/01_qc_cluster.R --outdir results
Rscript -e 'testthat::test_dir("tests/testthat")'   # the unit tests
quarto render report.qmd                             # renders the write-up to report.html
```

Requires R with `Seurat` (v5), `SeuratData`, `optparse`, and `testthat`, plus Quarto for the report.
In the real system this runs inside a pinned container so the environment is captured. Here it is kept
dependency-light on purpose. PBMC 3k is a standard 10x Genomics public dataset, also distributed
through the `SeuratData` package.

## What this example shows

- The approach and its thresholds are fixed before the data is touched, so there is no post-hoc
  tuning of cutoffs.
- The logic that decides which cells pass is a pure function with unit tests, so the core is verified
  rather than trusted.
- The result is checked against a stated expectation at output-QC and against known biology at
  bio-sense before it is believed.
- Every step leaves a committed record, so the analysis is auditable from start to finish.
