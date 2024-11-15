import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from fastapi import FastAPI

app = FastAPI()
movie = pd.read_csv("C:\\Users\\bikti\\Fazafilms.csv", low_memory=False)
new_df = movie[movie['userId'].map(movie['userId'].value_counts()) > 200]
users_pivot = new_df.pivot_table(index=["userId"],columns=["title"],values="rating")
users_pivot.fillna(0,inplace=True)
movieMatrix = csr_matrix(users_pivot.values)
movieMatrix = movieMatrix.transpose()

@app.get("/genre")
def read_root():
    all = {'Western', 'Thriller', 'War', 'Sci-Fi', 'Romance', 'Crime', 'Animation', 'Adventure',
           'Horror', 'Drama', 'Action', '(no genres listed)', 'Film-Noir', 'Comedy', 'Musical', 'Mystery',
           'IMAX', 'Children', 'Documentary', 'Fantasy'}
    return all

@app.get("/movie/top10")
def read_root():
    top_movies = top10().head(10)
    return top_movies.to_dict(orient='records')

@app.get("/movie/top10genre")
def read_item(genre: str):
    top_movies = top10genre(genre).head(10)
    return top_movies.to_dict(orient='records')

@app.get("/movie/top10rec")
def read_item(title: str):
    similar_movies = top10content(title).head(10)
    return similar_movies.to_dict(orient='records')



def top10():
    avg_ratings = movie.groupby('title')['rating'].mean().reset_index().rename(columns={'rating': 'avg_rating'})
    rating_counts = movie.groupby('title')['rating'].count().reset_index().rename(columns={'rating': 'rating_count'})
    avg=pd.DataFrame(avg_ratings).sort_values('avg_rating',ascending=False)
    avg = avg.merge(rating_counts, on='title')
    v=avg["rating_count"]
    R=avg["avg_rating"]
    m=v.quantile(0.90)
    c=R.mean()
    avg['w_score']=((v*R) + (m*c)) / (v+m)
    pop_sort=avg.sort_values('w_score',ascending=False)
    return pop_sort

def top10genre(genre: str):
    genre_movies = movie[movie['genres'].str.contains(genre)]
    avg_ratings = genre_movies.groupby('title')['rating'].mean().reset_index().rename(columns={'rating': 'avg_rating'})
    rating_counts = genre_movies.groupby('title')['rating'].count().reset_index().rename(columns={'rating': 'rating_count'})
    avg = pd.DataFrame(avg_ratings).sort_values('avg_rating', ascending=False)
    avg = avg.merge(rating_counts, on='title')
    v = avg["rating_count"]
    R = avg["avg_rating"]
    m = v.quantile(0.90)
    c = R.mean()
    avg['w_score'] = ((v * R) + (m * c)) / (v + m)
    pop_sort = avg.sort_values('w_score', ascending=False).head(10)
    return pop_sort

def top10content(movieTitle: str):
    model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
    model_knn.fit(movieMatrix)
    movieIndex = users_pivot.columns.get_loc(movieTitle)
    distances, indices = model_knn.kneighbors(movieMatrix[movieIndex], n_neighbors=11)
    similar_indices = indices[0][1:]
    similarMovie = [users_pivot.columns[idx] for idx in similar_indices]
    similarMovies=pd.DataFrame({"Фильм":similarMovie})
    return similarMovies




