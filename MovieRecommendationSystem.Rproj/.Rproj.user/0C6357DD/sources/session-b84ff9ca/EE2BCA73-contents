# =========================
# RECOMMENDATION GENERATION
# =========================

# Generate predictions
ubcf_pred <- predict(ubcf_model, rating_matrix, type = "ratings")
ibcf_pred <- predict(ibcf_model, rating_matrix, type = "ratings")

# Convert to matrices
ubcf_mat <- as(ubcf_pred, "matrix")
ibcf_mat <- as(ibcf_pred, "matrix")

# =========================
# HYBRID MODEL
# =========================

alpha <- 0.6
beta  <- 0.4

hybrid_matrix <- (alpha * ubcf_mat) + (beta * ibcf_mat)

# =========================
# USER-BASED RECOMMENDATION
# =========================

# Take User 1 (you can change dynamically later for API)
user_scores <- hybrid_matrix[1, ]

# Remove NA values (IMPORTANT FIX)
user_scores[is.na(user_scores)] <- 0

# Sort in descending order
user_sorted <- sort(user_scores, decreasing = TRUE)

# =========================
# FINAL RECOMMENDATION TABLE
# =========================

top_n <- 10

recommendations <- data.frame(
  Rank = 1:top_n,
  Movie = names(user_sorted)[1:top_n],
  Predicted_Rating = round(as.numeric(user_sorted[1:top_n]), 2),
  Match_Percentage = round(user_sorted[1:top_n] * 20, 2),
  Recommendation_Strength = ifelse(
    user_sorted[1:top_n] > 4, "High",
    ifelse(user_sorted[1:top_n] > 3, "Medium", "Low")
  )
)

# =========================
# OUTPUT PREVIEW
# =========================

print(recommendations)