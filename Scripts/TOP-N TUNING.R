setwd("C:/Users/ALEKYA/OneDrive/Desktop/MovieRecommendationSystem")

source("Scripts/global_config.R")
source("Scripts/Data_Preprocessing.R")
source("Scripts/User_Matrix.R")
source("Scripts/Model_Building.R")
str(rating_matrix)
class(rating_matrix)
rating_matrix <- as(rating_matrix, "realRatingMatrix")

ubcf_model <- Recommender(rating_matrix, method="UBCF")
ibcf_model <- Recommender(rating_matrix, method="IBCF")
topN <- c(5,10,15)

results <- lapply(topN, function(n){
  predict(ubcf_model, rating_matrix[1], n=n)
})