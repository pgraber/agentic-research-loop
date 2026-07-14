# Pure QC-filter logic — the deterministic core that DECIDES which cells pass.
# Kept as a pure function (no I/O, no Seurat object) precisely so it can be unit-tested:
# same inputs -> same logical vector, forever. See tests/testthat/test-qc_filters.R.

#' Which cells pass QC?
#'
#' @param n_feature integer vector, genes detected per cell
#' @param percent_mt numeric vector, mitochondrial read percentage per cell (0-100)
#' @param min_features,max_features inclusive gene-count bounds
#' @param max_percent_mt exclusive upper bound on mito percentage
#' @return logical vector, TRUE = keep. Any NA metric fails the cell (never silently kept).
cells_pass_qc <- function(n_feature, percent_mt,
                          min_features = 200, max_features = 2500,
                          max_percent_mt = 5) {
  if (length(n_feature) != length(percent_mt)) {
    stop("n_feature and percent_mt must be the same length")
  }
  keep <- n_feature >= min_features &
          n_feature <= max_features &
          percent_mt <  max_percent_mt
  keep[is.na(keep)] <- FALSE   # an unmeasurable cell fails, never passes by accident
  keep
}
