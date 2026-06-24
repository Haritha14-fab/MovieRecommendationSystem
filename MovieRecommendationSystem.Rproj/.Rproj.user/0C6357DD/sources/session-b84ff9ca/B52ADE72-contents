source("Scripts/global_config.R")

# User-item matrix
rating_matrix <- acast(
  data,
  userId ~ title,
  value.var = "rating",
  fun.aggregate = mean
)

# Convert to recommender format
rating_matrix <- as(rating_matrix, "realRatingMatrix")

# Sparsity calculation (CORRECT)
rating_mat <- as(rating_matrix, "matrix")

total_cells <- nrow(rating_mat) * ncol(rating_mat)

missing_values <- sum(is.na(rating_mat))

sparsity <- missing_values / total_cells

print(sparsity)