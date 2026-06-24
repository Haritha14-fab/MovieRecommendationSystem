source("Scripts/global_config.R")

# Safety check
if(!exists("rating_matrix")){
  stop("rating_matrix not found. Run User_Matrix.R first")
}

# UBCF Model (User-based)
ubcf_model <- Recommender(
  rating_matrix,
  method = "UBCF",
  parameter = list(method="cosine", nn=30)
)

# IBCF Model (Item-based)
ibcf_model <- Recommender(
  rating_matrix,
  method = "IBCF",
  parameter = list( method = "Cosine",k=30)
)

print("Models created successfully")