# Brief: PBMC 3k (worked example)

*In a real project this is `docs/.record/brief.md` (hidden, AI-facing). Shown here for the example.*

## Question (scope)
What immune cell populations are present in the 10x PBMC 3k dataset, and are the standard scRNA-seq
QC cutoffs defensible for it? The expected answer is a handful of clusters mapping to known PBMC
lineages (T, B, monocyte, NK, platelet).

## Grounding
This is a textbook demonstration dataset, so the method is the field-standard Seurat workflow rather
than a novel approach. The QC axes and cutoffs are community defaults, cited rather than invented:

- **Low `nFeature`** removes empty droplets and low-quality cells. **High `nFeature`** removes likely
  doublets.
- **High `percent.mt`** flags dying or stressed cells (mitochondrial leakage).
- The cutoffs `nFeature 200 to 2500` and `percent.mt < 5%` follow the Seurat PBMC 3k guided tutorial.

## Method intent
`NormalizeData → FindVariableFeatures → ScaleData → PCA(10) → FindNeighbors → FindClusters(0.5)`,
then annotate clusters by canonical lineage markers. The pipeline is deterministic, uses a fixed
seed, and the QC-decision function is unit-tested.

## Not in scope
Differential expression, trajectory, or any biological claim beyond "the expected lineages are
recovered". This example exists to demonstrate the *process*, not to produce a finding.
