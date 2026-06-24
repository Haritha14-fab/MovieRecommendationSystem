# Shared configuration for every R pipeline script.
# The Flask application expects the generated CSV files in Output/, so each
# R script should run from the project root. This keeps the project portable
# across different machines instead of depending on one absolute path.
args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(
  file_arg,
  "",
  args[grep(file_arg, args)]
)

if (length(script_path) > 0) {
  project_root <- normalizePath(
    file.path(dirname(script_path), ".."),
    winslash = "/",
    mustWork = TRUE
  )
} else {
  project_root <- normalizePath(
    getwd(),
    winslash = "/",
    mustWork = TRUE
  )
}

setwd(project_root)

library(dplyr)
library(reshape2)
library(recommenderlab)
library(ggplot2)
