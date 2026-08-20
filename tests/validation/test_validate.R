# Tests for the R validation helper. Run: Rscript test_validate.R
# Base R only, so it runs anywhere the analysis containers run.

here <- dirname(normalizePath(sub("^--file=", "",
  grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)[1])))
source(file.path(here, "..", "..", "templates", "project", "scripts", "validate.R"))

failures <- 0L
expect <- function(label, ok) {
  if (!isTRUE(ok)) {
    failures <<- failures + 1L
    cat("TEST FAIL:", label, "\n")
  } else {
    cat("test ok:", label, "\n")
  }
}
fails_with_error <- function(expr) inherits(try(expr, silent = TRUE), "try-error")

tmp <- file.path(tempdir(), "vtest")
dir.create(tmp, showWarnings = FALSE)
prefix <- file.path(tmp, "checks")

# --- exact pass, readable line ------------------------------------------------
vcheck_init(prefix, step = "test")
vcheck("transcripts", 50000, 50000, source = "GENCODE v44")
text <- paste(readLines(paste0(prefix, ".log")), collapse = "\n")
expect("pass is logged", grepl("PASS", text))
expect("count is thousands-separated", grepl("transcripts: 50,000 \\(expected 50,000\\)", text))
expect("source is recorded", grepl("\\[GENCODE v44\\]", text))

# --- a mismatch stops the run -------------------------------------------------
expect("off-by-one fails", fails_with_error(vcheck("transcripts", 49999, 50000)))
expect("zero is not silently truthy", fails_with_error(vcheck("cells", 0, 5000)))

# --- tolerance band edges -----------------------------------------------------
vcheck_init(prefix, step = "test")
expect("inside tolerance passes", isTRUE(vcheck("proportion", 0.51, 0.50, tol = 0.01)))
expect("outside tolerance fails", fails_with_error(vcheck("proportion", 0.52, 0.50, tol = 0.01)))

# --- logical assertions -------------------------------------------------------
vcheck_init(prefix, step = "test")
expect("set equality passes", isTRUE(vcheck("ids preserved", setequal(1:2, 2:1), TRUE)))
expect("set inequality fails", fails_with_error(vcheck("ids preserved", setequal(1:2, c(1, 3)), TRUE)))
expect("NA actual fails", fails_with_error(vcheck("count", NA_integer_, 10)))

# --- warn_only records but continues -----------------------------------------
vcheck_init(prefix, step = "test")
expect("warn_only returns FALSE", identical(vcheck("optional", 5, 6, warn_only = TRUE), FALSE))
expect("warn is logged", any(grepl("^WARN", readLines(paste0(prefix, ".log")))))

# --- machine-readable tsv -----------------------------------------------------
vcheck_init(prefix, step = "01_load")
vcheck("transcripts", 50000, 50000, source = "GENCODE v44")
rows <- readLines(paste0(prefix, ".tsv"))
expect("tsv header", identical(strsplit(rows[1], "\t")[[1]],
  c("status", "timestamp", "step", "label", "actual", "expected", "source")))
f <- strsplit(rows[2], "\t")[[1]]
expect("tsv row fields", f[1] == "PASS" && f[3] == "01_load" && f[4] == "transcripts" &&
  f[7] == "GENCODE v44")

# --- summary tally ------------------------------------------------------------
vcheck_init(prefix, step = "test")
vcheck("a", 1, 1)
vcheck("b", 2, 3, warn_only = TRUE)
tally <- vcheck_summary()
expect("tally counts", identical(tally, list(pass = 1L, fail = 1L)))
expect("tally line", any(grepl("2 checks: 1 passed, 1 failed", readLines(paste0(prefix, ".log")))))

# --- init truncates a previous log -------------------------------------------
vcheck_init(prefix, step = "first")
vcheck("a", 1, 1)
vcheck_init(prefix, step = "second")
expect("log truncated", !grepl("first", paste(readLines(paste0(prefix, ".log")), collapse = "")))
expect("tsv truncated", length(readLines(paste0(prefix, ".tsv"))) == 1L)

cat(if (failures == 0L) "\nall R validation tests passed\n" else
    sprintf("\n%d R validation tests FAILED\n", failures))
quit(status = if (failures == 0L) 0L else 1L)
