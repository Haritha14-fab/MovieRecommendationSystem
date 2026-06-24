ggplot(data,
       aes(x = rating)) +
  geom_histogram(binwidth = 1)

ggplot(movie_stats,
       aes(x = reorder(title, avg_rating),
           y = avg_rating)) +
  geom_col() +
  coord_flip() 
