#!/usr/bin/env Rscript
# 01_qc_cluster.R — QC + clustering of 10x PBMC 3k, applying the PRE-REGISTERED thresholds
# from the design checkpoint (docs/checkpoints.md). The QC decision logic lives in
# scripts/functions/qc_filters.R and is unit-tested — this script only orchestrates.
# Targets Seurat v5. Run from examples/pbmc3k:  Rscript scripts/01_qc_cluster.R --outdir results
suppressPackageStartupMessages({ library(optparse); library(Seurat) })

opt <- parse_args(OptionParser(option_list = list(
  make_option("--data",           default = NULL, help = "10x filtered matrix dir; if omitted, load via SeuratData"),
  make_option("--outdir",         default = "results", help = "output dir [%default]"),
  make_option("--min_features",   type = "integer", default = 200L),
  make_option("--max_features",   type = "integer", default = 2500L),
  make_option("--max_percent_mt", type = "double",  default = 5),
  make_option("--npcs",           type = "integer", default = 10L),
  make_option("--resolution",     type = "double",  default = 0.5),
  make_option("--seed",           type = "integer", default = 42L)
)))

set.seed(opt$seed)                                    # reproducibility: fixed seed
dir.create(opt$outdir, showWarnings = FALSE, recursive = TRUE)
source("scripts/functions/qc_filters.R")

## --- load ---
if (!is.null(opt$data)) {
  pbmc <- CreateSeuratObject(Read10X(opt$data), project = "pbmc3k", min.cells = 3, min.features = 200)
} else {
  if (!requireNamespace("SeuratData", quietly = TRUE))
    stop("Get the data: install SeuratData then SeuratData::InstallData('pbmc3k'), or pass --data <10x dir>.")
  pbmc <- UpdateSeuratObject(SeuratData::LoadData("pbmc3k"))
}

## --- intake-QC (sanity: expect ~2,700 cells) ---
message(sprintf("Loaded %d cells x %d genes", ncol(pbmc), nrow(pbmc)))

## --- per-cell metrics + PRE-REGISTERED QC via the unit-tested pure function ---
pbmc[["percent.mt"]] <- PercentageFeatureSet(pbmc, pattern = "^MT-")
keep <- cells_pass_qc(pbmc$nFeature_RNA, pbmc$percent.mt,
                      opt$min_features, opt$max_features, opt$max_percent_mt)
message(sprintf("QC: %d/%d cells pass (nFeature %d-%d, percent.mt < %g)",
                sum(keep), length(keep), opt$min_features, opt$max_features, opt$max_percent_mt))
pbmc <- pbmc[, keep]

## --- standard pipeline ---
pbmc <- NormalizeData(pbmc, verbose = FALSE)
pbmc <- FindVariableFeatures(pbmc, verbose = FALSE)
pbmc <- ScaleData(pbmc, verbose = FALSE)
pbmc <- RunPCA(pbmc, npcs = opt$npcs, verbose = FALSE)
pbmc <- FindNeighbors(pbmc, dims = seq_len(opt$npcs), verbose = FALSE)
pbmc <- FindClusters(pbmc, resolution = opt$resolution, verbose = FALSE)

## --- output-QC numbers → results/ (so the write-up can trace every figure it quotes) ---
qc <- data.frame(
  n_cells_loaded    = length(keep),
  n_cells_pass      = sum(keep),
  n_clusters        = nlevels(Idents(pbmc)),
  median_nFeature   = median(pbmc$nFeature_RNA),
  median_percent_mt = round(median(pbmc$percent.mt), 3)
)
write.csv(qc, file.path(opt$outdir, "qc_summary.csv"), row.names = FALSE)

## --- bio-sense: do the EXPECTED PBMC lineage markers light up? ---
markers <- c("MS4A1", "CD3D", "CD14", "FCGR3A", "NKG7", "PPBP")  # B, T, mono, FCGR3A+ mono, NK, platelet
present <- intersect(markers, rownames(pbmc))
avg <- AverageExpression(pbmc, features = present, assay = "RNA")[["RNA"]]
write.csv(as.data.frame(avg), file.path(opt$outdir, "marker_avg_expression.csv"))

saveRDS(pbmc, file.path(opt$outdir, "pbmc3k_clustered.rds"))
message("Wrote qc_summary.csv, marker_avg_expression.csv, pbmc3k_clustered.rds to ", opt$outdir)
