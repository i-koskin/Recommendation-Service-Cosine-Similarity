from typing import List, Set, AnyStr

import streamlit as st
import pandas as pd
from .utils import parse
import ast

@st.cache_data  # Кэширование данных для ускорения работы
def _load_base(path: str, index_col: str = 'id') -> pd.DataFrame:
    # Загрузка CSV файла в DataFrame с указанным индексом
    db = pd.read_csv(path, index_col=index_col)
    db.index = db.index.astype(int)  # Приведение индекса к типу int
    return db  # Возврат загруженного DataFrame

class ContentBaseRecSys:
    # Инициализация класса для системы рекомендаций на основе контента
    def init(self, movies_dataset_filepath: str, distance_filepath: str):
        self.distance_1 = _load_base(distance_filepath, index_col='id')  # Загрузка дистанционной матрицы
        # self.distance.index = self.distance.index.astype(int)  
        self.distance_1.columns = self.distance_1.columns.astype(int)  # Приведение названий столбцов к типу int
        self.distance = self.distance_1  # Сохранение дистанционной матрицы
        self._init_movies(movies_dataset_filepath)  # Инициализация данных о фильмах

    def _init_movies(self, movies_dataset_filepath) -> None:
        # Инициализация данных о фильмах
        self.movies_1 = _load_base(movies_dataset_filepath, index_col='id')  # Загрузка данных о фильмах
        # self.movies.index = self.movies.index.astype(int)  # Приведение индекса к типу int (закомментировано)
        self.movies_1['genres'] = self.movies_1['genres'].apply(parse)  # Парсинг жанров фильмов
        self.movies_1['years'] = pd.DatetimeIndex(self.movies_1.release_date).year.fillna(0).astype(int)  # Извлечение годов выпуска
        self.movies_1['title_year'] = self.movies_1['title'] + ' (' + self.movies_1['years'].astype(str) + ')'  # Формирование заголовка с годом
        self.movies_1['director'] = self.movies_1['crew'].apply(lambda x: ', '.join([i['name'] for i in ast.literal_eval(x) if i['job'] == 'Director']))  # Извлечение имен режиссеров
        self.movies = self.movies_1  # Сохранение данных о фильмах

    def get_titles(self) -> List[str]:
        # Получение списка названий фильмов
        return self.movies_1['title_year'].values

    def get_genres(self) -> Set[str]:
        # Получение уникального набора жанров фильмов
        genres = [item for sublist in self.movies_1['genres'].values.tolist() for item in sublist] 
        return set(genres)  
    
    def get_years(self) -> Set[str]:
        # Получение уникального набора годов выхода фильмов
        return set(self.movies_1.years)
    
    def get_list_directors(self) -> List[str]:
        # Получение списка уникальных режиссеров
        return self.movies_1['director'].unique()
    
    def get_directors(self) -> Set[str]:
        # Получение уникального набора режиссеров
        return set(self.movies_1.director)

    def get_film_id(self, title_year: str) -> int:
        # Получение идентификатора фильма по названию и году
        return self.movies_1.loc[self.movies_1.title_year == title_year].index[0]
    
    def get_film_year(self, id: int) -> int:
        # Получение года выхода фильма по его идентификатору
        return self.movies_1.loc[id].years
    
    def get_film_directors(self, id: int) -> List[str]:
        # Получение списка режиссеров фильма по его идентификатору
        return self.movies_1.loc[id].director
    
    def get_film_genres(self, id: int) -> List[str]:
        # Получение списка жанров фильма по его идентификатору
        return self.movies_1.loc[id].genres
    
    def get_film_title(self, id: int) -> AnyStr:
        # Получение названия фильма по его идентификатору
        return self.movies_1.loc[id].original_title
    
    def get_film_overview(self, id: int) -> AnyStr:
        # Получение описания фильма по его идентификатору
        return self.movies_1.loc[id].overview
   
    def set_filter(self, director: str, year: int, genre: str) -> None:
        # Установка фильтров для данных о фильмах
        self.movies = self.movies_1
        if director: 
            self.movies = self.movies.loc[self.movies.director == director]  # Фильтрация по режиссеру
        if year:  
            self.movies = self.movies.loc[self.movies.years == year]  # Фильтрация по году
        if genre:  
            self.movies = self.movies.loc[self.movies.genres.apply(lambda x: genre in x)]  # Фильтрация по жанру
        self.distance = self.distance.loc[self.movies.index]  # Обновление дистанционной матрицы

    def remove_filter(self) -> None:
        # Сброс фильтров
        self.movies = self.movies_1  # Восстановление исходного списка фильмов
        self.distance = self.distance_1  # Восстановление исходной дистанционной матрицы

    def recommendation(self, title_year: str, top_k: int = 5) -> List[str]:
        """
        Возвращает названия top_k наиболее похожих фильмов на фильм  
        """
        ind = pd.Series(self.movies_1.index, index=self.movies_1['title_year'])  # Создание серии индекс-значение по названиям фильмов
        idx = ind[title_year]  # Получение индекса фильма по названию
        sim_scores = list(enumerate(self.distance[idx]))  # Получение оценок схожести с другими фильмами
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)  # Сортировка по убыванию схожести
        sim_scores = sim_scores[1:(top_k + 1)]  # Выбор top_k фильмов (пропускаем первый, так как это сам фильм)
        movie_ind = [i[0] for i in sim_scores]  # Извлечение индексов фильмов
        return list(self.movies['title_year'].iloc[movie_ind])  # Возврат названий фильмов
