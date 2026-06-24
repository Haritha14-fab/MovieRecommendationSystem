neighbors <- c(10,20,30,40,50)

results <- data.frame()

for(n in neighbors){
  
  model <- Recommender(
    rating_matrix,
    method="UBCF",
    parameter=list(
      method="Cosine",
      nn=n
    )
  )
  
  pred <-
    predict(
      model,
      rating_matrix[1],
      n=10
    )
  
  results <-
    rbind(
      results,
      data.frame(
        Neighbors=n
      )
    )
}

optimization_results <- results

print(optimization_results)