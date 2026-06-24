import pandas as pd
import numpy as np

ratings = pd.read_csv(
    "../Dataset/ml-100k/u.data",
    sep="\t",
    header=None,
    names=["userId","movieId","rating","timestamp"]
)

mean_rating = np.mean(ratings["rating"])

print("Average Rating:", mean_rating)
