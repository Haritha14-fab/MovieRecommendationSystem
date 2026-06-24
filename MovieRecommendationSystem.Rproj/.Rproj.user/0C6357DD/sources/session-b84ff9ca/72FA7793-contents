source("Scripts/global_config.R")
library(recommenderlab)

# =========================
# CHECK DATA
# =========================
if(!exists("rating_matrix")){
  stop("rating_matrix not found. Run User_Matrix.R first")
}

# =========================
# TRAIN MODELS
# =========================
ubcf_model <- Recommender(rating_matrix, method = "UBCF")
ibcf_model <- Recommender(rating_matrix, method = "IBCF")

cat("Models trained successfully\n")

# =========================
# PREDICT RATINGS
# =========================
ubcf_pred <- predict(ubcf_model, rating_matrix, type = "ratings")
ibcf_pred <- predict(ibcf_model, rating_matrix, type = "ratings")

ubcf_mat <- as(ubcf_pred, "matrix")
ibcf_mat <- as(ibcf_pred, "matrix")

# =========================
# HYBRID MODEL (FINAL CORRECT)
# =========================
alpha <- 0.6
beta  <- 0.4

hybrid_matrix <- (alpha * ubcf_mat) + (beta * ibcf_mat)

cat("Hybrid Model Created Successfully\n")

# Preview output
hybrid_matrix[1:5, 1:5]