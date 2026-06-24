source("Scripts/global_config.R")

# Rating distribution
table(data$rating)

# Average rating per movie
movie_stats <- data %>%
  group_by(title) %>%
  summarise(avg_rating = mean(rating), count = n()) %>%
  arrange(desc(avg_rating))

head(movie_stats, 10)

# Most active users
user_stats <- data %>%
  group_by(userId) %>%
  summarise(count = n()) %>%
  arrange(desc(count))

head(user_stats, 10)

# Visualization
ggplot(data, aes(x=rating)) +
  geom_histogram(binwidth=1, fill="blue", color="white")