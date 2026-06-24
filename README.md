# Movie Recommendation System

This project is a Flask-based Movie Recommendation System built for a Data Science minor project. It uses the MovieLens 100k dataset, R-based collaborative filtering scripts, Python/Flask API endpoints, poster lookup through OMDb, and responsive HTML pages.

## Recommendation Type

The system follows a hybrid recommendation approach:

- Content-based similarity in Python recommends movies similar to the searched title.
- Collaborative filtering in R uses user-based collaborative filtering and item-based collaborative filtering.
- Hybrid scoring combines R UBCF and IBCF predictions with weights `alpha = 0.6` and `beta = 0.4`.

The Flask app now reads the R-generated `Output/recommendations.csv` first, so the `.R` files are part of the live recommendation flow. If the R output is missing, Flask attempts to run `Scripts/Run_All.R` with `Rscript`.

## Dataset

The project uses MovieLens 100k files:

- `Dataset/ml-100k/u.data`: user ratings with `userId`, `movieId`, `rating`, and timestamp.
- `Dataset/ml-100k/u.item`: movie metadata with titles and genre flags.

## Data Science Pipeline

The R pipeline is organized step by step:

1. `Scripts/Data_Preprocessing.R`: loads ratings and movies, handles missing values, creates movie genres, removes duplicates, and normalizes ratings.
2. `Scripts/EDA.R` and `Scripts/Visualization.R`: support exploratory analysis of ratings and movie interactions.
3. `Scripts/User_Matrix.R`: builds the user-item rating matrix.
4. `Scripts/Model_Building.R`: trains UBCF and IBCF recommenderlab models.
5. `Scripts/Recommendation.R`: generates predicted ratings and top-N recommendations.
6. `Scripts/Hybrid_model.R`: combines UBCF and IBCF outputs into a hybrid matrix.
7. `Scripts/Evaluation.R`: evaluates recommendation accuracy with RMSE, MSE, and MAE.
8. `Scripts/Optimization.R`: tests neighbor-count tuning for scalability.
9. `Scripts/Documentation.R`: records design points and limitations.
10. `Scripts/Output_Generation.R`: writes final CSV outputs for Flask.

Run the full R pipeline:

```powershell
Rscript Scripts/Run_All.R
```

Generated outputs:

- `Output/recommendations.csv`
- `Output/hybrid_matrix.csv`
- `Output/evaluation_results.csv`
- `Output/optimization_results.csv`
- `Output/ubcf_model.rds`
- `Output/ibcf_model.rds`

## Flask Pages

- `/`: main page with movie search, suggestions, poster cards, and the Get Recommendations button.
- `/search.html?title=Movie+Name`: displays the searched movie first and then recommended movies.
- `/recommendation.html?title=Movie+Name`: opens the recommendation page.
- `/movie.html?title=Movie+Name`: opens movie details, poster, plot, trailer/watch links, and similar movies.
- `/movie/<title>`: alternate movie detail route.

## API Endpoints

The frontend is connected to these API endpoints:

- `GET /api/title_suggest?q=bat`: returns movie-name suggestions.
- `GET /api/search?q=bat`: returns matching movie names.
- `GET /api/recommend?title=Toy+Story+(1995)&topn=12`: returns R hybrid recommendations plus Python similarity fallback.
- `GET /api/recommend_ai?title=Toy+Story+(1995)&topn=10`: returns Python recommendation results.
- `GET /api/poster?title=Toy+Story+(1995)`: returns a poster URL from OMDb.
- `GET /api/r/status`: reports whether R output files exist.
- `POST /api/run_r`: runs selected R scripts such as `Run_All`, `Recommendation`, `Hybrid_model`, or `Evaluation`.

## Setup

Install Python dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Install required R packages:

```r
install.packages(c("dplyr", "reshape2", "recommenderlab", "ggplot2"))
```

Run the R pipeline:

```powershell
Rscript Scripts/Run_All.R
```

Start Flask:

```powershell
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Poster Support

Posters are fetched from the internet through OMDb using the configured `OMDB_API_KEY` in `app.py`. If a poster is unavailable, the app displays `static/images/no-poster.svg`.

## Mobile Responsiveness

The UI uses Bootstrap grid classes and custom responsive CSS. On mobile screens, search controls stack vertically, posters resize, and movie cards remain readable.

## Limitations

- New users may receive generic R recommendations until enough ratings are available.
- MovieLens 100k is small, so recommendations are useful for a project demo but not production-scale personalization.
- OMDb poster availability depends on internet access and API limits.
- R pipeline execution requires R and the listed R packages to be installed.
