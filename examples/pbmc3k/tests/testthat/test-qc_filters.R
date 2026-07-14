# Unit tests for the pure QC-filter core. Run: testthat::test_dir("tests/testthat")
source(file.path("..", "..", "scripts", "functions", "qc_filters.R"))

test_that("cells inside all bounds pass", {
  expect_equal(
    cells_pass_qc(n_feature = c(500, 1000), percent_mt = c(2, 4)),
    c(TRUE, TRUE)
  )
})

test_that("each boundary is enforced", {
  # below min features, above max features, at/over mito ceiling
  expect_equal(
    cells_pass_qc(n_feature = c(199, 2501, 800), percent_mt = c(1, 1, 5)),
    c(FALSE, FALSE, FALSE)
  )
})

test_that("inclusive feature bounds, exclusive mito bound", {
  expect_true(cells_pass_qc(200, 4.99))    # lower feature bound inclusive
  expect_true(cells_pass_qc(2500, 0))      # upper feature bound inclusive
  expect_false(cells_pass_qc(800, 5))      # mito bound is exclusive
})

test_that("NA metrics fail closed (never silently kept)", {
  expect_equal(
    cells_pass_qc(n_feature = c(NA, 800), percent_mt = c(2, NA)),
    c(FALSE, FALSE)
  )
})

test_that("mismatched lengths error rather than recycle", {
  expect_error(cells_pass_qc(c(500, 600), 2), "same length")
})
