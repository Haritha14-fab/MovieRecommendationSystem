source("Scripts/global_config.R")

# Load ratings
ratings <- read.table(
  "Dataset/ml-100k/u.data",
  sep = "\t",
  header = FALSE,
  col.names = c(
    "userId",
    "movieId",
    "rating",
    "timestamp"
  )
)

# Load movies
movies <- read.table(
  "Dataset/ml-100k/u.item",
  sep = "|",
  header = FALSE,
  fill = TRUE,
  quote = "",
  fileEncoding = "latin1"
)

# Genre column names
genre_cols <- c(
  "unknown",
  "Action",
  "Adventure",
  "Animation",
  "Children",
  "Comedy",
  "Crime",
  "Documentary",
  "Drama",
  "Fantasy",
  "FilmNoir",
  "Horror",
  "Musical",
  "Mystery",
  "Romance",
  "SciFi",
  "Thriller",
  "War",
  "Western"
)

# Assign names to genre columns
colnames(movies)[6:24] <- genre_cols

# Rename first columns
colnames(movies)[1] <- "movieId"
colnames(movies)[2] <- "title"

# Create Genre column
movies$Genre <- apply(
  movies[, genre_cols],
  1,
  function(x) {
    
    genres <- genre_cols[x == 1]
    
    if (length(genres) == 0) {
      return("Unknown")
    }
    
    paste(
      genres,
      collapse = "/"
    )
  }
)

# Keep only required columns
movies <- movies[, c(
  "movieId",
  "title",
  "Genre"
)]

# Merge datasets
data <- merge(
  ratings,
  movies,
  by = "movieId"
)

# Cleaning
data <- na.omit(data)
data <- distinct(data)

# Keep required columns
data <- data[, c(
  "userId",
  "movieId",
  "rating",
  "title",
  "Genre"
)]

# Normalize ratings
data$rating_normalized <-
  (data$rating - min(data$rating)) /
  (max(data$rating) - min(data$rating))

# Preview
head(data)