from typing import List, Set, AnyStr

import streamlit as st
import pandas as pd
from .utils import parse
import ast

@st.cache_data
def _load_base(path: str, index_col: str= 'id') -> pd.DataFrame:
    db = pd.read_csv(path, index_col= index_col)
    db.index = db.index.astype(int)
    return db

class ContentBaseRecSys:

    def __init__(self, movies_dataset_filepath: str, distance_filepath: str):
        self.distance_1 = _load_base(distance_filepath, index_col= 'id')
        # self.distance.index = self.distance.index.astype(int)
        self.distance_1.columns = self.distance_1.columns.astype(int)
        self.distance = self.distance_1
        self._init_movies(movies_dataset_filepath)

    def _init_movies(self, movies_dataset_filepath) -> None:
        self.movies_1 = _load_base(movies_dataset_filepath, index_col='id')
        # self.movies.index = self.movies.index.astype(int)
        self.movies_1['genres'] = self.movies_1['genres'].apply(parse)
        self.movies_1['years'] = pd.DatetimeIndex(self.movies_1.release_date).year.fillna(0).astype(int)
        self.movies_1['title_year'] = self.movies_1['title'] + ' ('+self.movies_1['years'].astype(str)+')'
        self.movies_1['director'] = self.movies_1['crew'].apply(lambda x: ', '.join([i['name'] for i in ast.literal_eval(x) if i['job'] == 'Director']))
        self.movies = self.movies_1

    def get_titles(self) -> List[str]:
        return self.movies_1['title_year'].values

    def get_genres(self) -> Set[str]:
        genres = [item for sublist in self.movies_1['genres'].values.tolist() for item in sublist]
        return set(genres)
    
    def get_years(self) -> Set[str]:
        return set(self.movies_1.years)
    
    def get_list_directors(self) -> List[str]:
        return self.movies_1['director'].unique()
    
    def get_directors(self) -> Set[str]:
        return set(self.movies_1.director)

    def get_film_id(self, title_year: str) -> int:
        return self.movies_1.loc[self.movies_1.title_year == title_year].index[0]
    
    def  get_film_year(self, id: int) -> int:
        return self.movies_1.loc[id].years
    
    def get_film_directors(self, id: int) -> List[str]:
        return self.movies_1.loc[id].director
    
    def get_film_genres(self, id: int) -> List[str]:
        return self.movies_1.loc[id].genres
    
    def get_film_title(self, id: int) -> AnyStr:
        return self.movies_1.loc[id].original_title
    
    def get_film_overview(self, id: int) -> AnyStr:
        return self.movies_1.loc[id].overview
   
    def set_filter(self, director: str, year: int, genre: str) -> None:
        self.movies = self.movies_1
        if director:
            self.movies = self.movies.loc[self.movies.director == director]
        if year:
            self.movies = self.movies.loc[self.movies.years == year]
        if genre:
            self.movies = self.movies.loc[self.movies.genres.apply(lambda x: genre in x)]
        self.distance = self.distance.loc[self.movies.index]
        

    def remove_filter(self) -> None:
        self.movies = self.movies_1
        self.distance = self.distance_1

    def recommendation(self, title_year: str, top_k: int = 5) -> List[str]:
        """
        Returns the names of the top_k most similar movies with the movie "title"
        """
        ind = pd.Series(
            self.movies_1.index, index= self.movies_1['title_year'])
        idx = ind[title_year]
        sim_scores = list(enumerate(self.distance[idx]))
        sim_scores = sorted(sim_scores, key= lambda x: x[1], reverse= True)
        sim_scores = sim_scores[1:(top_k + 1)]
        movie_ind = [i[0] for i in sim_scores]
        return list(self.movies['title_year'].iloc[movie_ind])
