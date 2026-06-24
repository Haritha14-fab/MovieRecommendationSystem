# Create Output folder if it doesn't exist
if (!dir.exists("Output")) {
  dir.create("Output")
}

# Save recommendations
if (exists("recommendations")) {
  
  write.csv(
    recommendations,
    "Output/recommendations.csv",
    row.names = FALSE
  )
  
  cat("recommendations.csv created\n")
  
} else {
  cat("Error: recommendations object not found.\n")
}


# Save evaluation results
if (exists("evaluation_results")) {
  
  write.csv(
    evaluation_results,
    "Output/evaluation_results.csv",
    row.names = FALSE
  )
  
  cat("evaluation_results.csv created\n")
}


# Save optimization results
if (exists("optimization_results")) {
  
  write.csv(
    optimization_results,
    "Output/optimization_results.csv",
    row.names = FALSE
  )
  
  cat("optimization_results.csv created\n")
}


# Check saved models
if (file.exists("Output/ubcf_model.rds")) {
  cat("ubcf_model.rds exists\n")
}


if (file.exists("Output/ibcf_model.rds")) {
  cat("ibcf_model.rds exists\n")
}