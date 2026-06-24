source("Scripts/Python_Integration.R")
source("Scripts/global_config.R")
source("Scripts/Data_Preprocessing.R")
source("Scripts/EDA.R")
source("Scripts/Visualization.R")
source("Scripts/User_Matrix.R")
source("Scripts/Content_Based_Model.R")
source("Scripts/Model_Building.R")
source("Scripts/Recommendation.R")
source("Scripts/Evaluation.R")
source("Scripts/Hybrid_model.R")
source("Scripts/Optimization.R")
source("Scripts/Documentation.R")
source("Scripts/Output_Generation.R")
# Save hybrid output for Python API
# Ensure Output folder exists
if(!dir.exists("Output")){
  dir.create("Output")
}

# Save hybrid matrix
write.csv(
  hybrid_matrix,
  "Output/hybrid_matrix.csv",
  row.names = FALSE
)

cat("Hybrid matrix saved successfully\n")
write.csv(
  recommendations,
  "Output/recommendations.csv",
  row.names = FALSE
)

cat("Final recommendations saved\n")
