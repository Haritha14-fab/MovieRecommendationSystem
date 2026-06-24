source("Scripts/global_config.R")

scheme <- evaluationScheme(
  rating_matrix,
  method = "split",
  train = 0.8,
  given = 10,
  goodRating = 4
)

train <- getData(scheme, "train")
test_known <- getData(scheme, "known")
test_unknown <- getData(scheme, "unknown")

# Train models
ubcf <- Recommender(train, "UBCF")
ibcf <- Recommender(train, "IBCF")

# Predictions
pred_ubcf <- predict(ubcf, test_known, type="ratings")
pred_ibcf <- predict(ibcf, test_known, type="ratings")

acc_ubcf <- calcPredictionAccuracy(
  pred_ubcf,
  test_unknown
)

acc_ibcf <- calcPredictionAccuracy(
  pred_ibcf,
  test_unknown
)

evaluation_results <- data.frame(
  Model = c("UBCF", "IBCF"),
  RMSE = c(acc_ubcf["RMSE"], acc_ibcf["RMSE"]),
  MSE = c(acc_ubcf["MSE"], acc_ibcf["MSE"]),
  MAE = c(acc_ubcf["MAE"], acc_ibcf["MAE"])
)

print(evaluation_results)
# Save trained models
saveRDS(
  ubcf_model,
  "Output/ubcf_model.rds"
)

saveRDS(
  ibcf_model,
  "Output/ibcf_model.rds"
)

cat("Models saved successfully.\n")