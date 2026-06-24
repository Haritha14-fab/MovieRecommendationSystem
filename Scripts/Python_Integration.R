# Optional bridge for teams that want to inspect Python libraries from R.
# The recommendation pipeline itself is implemented in R and must continue
# even when reticulate or a local Python installation is unavailable.
if (requireNamespace("reticulate", quietly = TRUE)) {
  
  library(reticulate)
  
  py_config()
  
  pd <- import("pandas", delay_load = TRUE)
  np <- import("numpy", delay_load = TRUE)
  
  cat("Optional Python bridge configured\n")
  
} else {
  
  cat("reticulate not installed; continuing with the R recommendation pipeline\n")
  
}
