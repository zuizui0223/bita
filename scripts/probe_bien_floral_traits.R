# Probe BIEN's live trait catalog for floral / attraction traits.
#
# This is a source-contract test. It does not assume that a trait name such as
# "flower" implies an attraction measurement; the retained rows are exported
# for manual semantic review before any network join.

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 1) {
  stop("usage: Rscript scripts/probe_bien_floral_traits.R out_dir", call. = FALSE)
}
out_dir <- args[[1]]
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

if (!requireNamespace("BIEN", quietly = TRUE)) {
  stop("BIEN package is not installed", call. = FALSE)
}

catalog <- BIEN::BIEN_trait_list()
if (!is.data.frame(catalog) || nrow(catalog) == 0) {
  stop("BIEN_trait_list returned no trait rows", call. = FALSE)
}

names_lower <- tolower(names(catalog))
text_columns <- names(catalog)[vapply(catalog, function(x) is.character(x) || is.factor(x), logical(1))]
needle <- "flower|floral|corolla|petal|nectar|inflorescence|display|pollin|colour|color"
row_text <- apply(catalog[, text_columns, drop = FALSE], 1, function(row) paste(row, collapse = " | "))
floral_hits <- catalog[grepl(needle, row_text, ignore.case = TRUE), , drop = FALSE]

write.csv(catalog, file.path(out_dir, "bien_trait_catalog.csv"), row.names = FALSE, na = "")
write.csv(floral_hits, file.path(out_dir, "bien_floral_trait_candidates.csv"), row.names = FALSE, na = "")

report <- list(
  source = "BIEN::BIEN_trait_list",
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
)
jsonlite::write_json(report, file.path(out_dir, "bien_floral_trait_probe.json"), pretty = TRUE, auto_unbox = TRUE)
cat(jsonlite::toJSON(report, pretty = TRUE, auto_unbox = TRUE), "\n")
