# Probe BIEN's live trait catalog for floral / attraction traits.
#
# This is a source-contract test. It does not assume that a trait name such as
# "flower" implies an attraction measurement; retained rows require manual
# semantic review before any network join. A remote-query failure is a valid
# result of the source test, not a CI failure: it is recorded and causes an
# explicit pivot away from BIEN as an automated backbone.

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 1) {
  stop("usage: Rscript scripts/probe_bien_floral_traits.R out_dir", call. = FALSE)
}
out_dir <- args[[1]]
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

write_report <- function(report) {
  jsonlite::write_json(
    report,
    file.path(out_dir, "bien_floral_trait_probe.json"),
    pretty = TRUE,
    auto_unbox = TRUE
  )
  cat(jsonlite::toJSON(report, pretty = TRUE, auto_unbox = TRUE), "\n")
}

if (!requireNamespace("BIEN", quietly = TRUE)) {
  write_report(list(
    source = "BIEN::BIEN_trait_list",
    access_status = "package_unavailable",
    decision = "reject_BIEN_for_automated_floral_trait_backbone_and_pivot"
  ))
  quit(status = 0)
}

catalog_result <- tryCatch(
  list(value = BIEN::BIEN_trait_list(), error = NULL),
  error = function(error) list(value = NULL, error = error)
)

if (!is.null(catalog_result$error)) {
  write_report(list(
    source = "BIEN::BIEN_trait_list",
    access_status = "remote_query_failed",
    error_class = class(catalog_result$error)[[1]],
    error_message = conditionMessage(catalog_result$error),
    decision = "reject_BIEN_for_automated_floral_trait_backbone_and_pivot"
  ))
  quit(status = 0)
}

catalog <- catalog_result$value
if (!is.data.frame(catalog) || nrow(catalog) == 0) {
  write_report(list(
    source = "BIEN::BIEN_trait_list",
    access_status = "empty_catalog",
    decision = "reject_BIEN_for_automated_floral_trait_backbone_and_pivot"
  ))
  quit(status = 0)
}

text_columns <- names(catalog)[vapply(catalog, function(x) is.character(x) || is.factor(x), logical(1))]
needle <- "flower|floral|corolla|petal|nectar|inflorescence|display|pollin|colour|color"
row_text <- apply(catalog[, text_columns, drop = FALSE], 1, function(row) paste(row, collapse = " | "))
floral_hits <- catalog[grepl(needle, row_text, ignore.case = TRUE), , drop = FALSE]

write.csv(catalog, file.path(out_dir, "bien_trait_catalog.csv"), row.names = FALSE, na = "")
write.csv(floral_hits, file.path(out_dir, "bien_floral_trait_candidates.csv"), row.names = FALSE, na = "")

write_report(list(
  source = "BIEN::BIEN_trait_list",
  access_status = "ok",
  catalog_rows = nrow(catalog),
  catalog_columns = names(catalog),
  text_columns_screened = text_columns,
  floral_keyword = needle,
  floral_candidate_rows = nrow(floral_hits),
  decision = if (nrow(floral_hits) > 0) {
    "advance_to_species_coverage_test_after_manual_semantic_review"
  } else {
    "reject_BIEN_for_floral_trait_backbone_and_pivot_to_trait_first_source"
  }
))