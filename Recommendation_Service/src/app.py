import os

import streamlit as st
from streamlit_extras.no_default_selectbox import selectbox
from streamlit_extras.add_vertical_space import add_vertical_space

from dotenv import load_dotenv

from PIL import Image
from api.omdb import OMDBApi
from recsys import ContentBaseRecSys

TOP_K = 5  # Устанавливаем максимальное количество рекомендаций
load_dotenv()  # Загружаем переменные окружения из .env файла

API_KEY = os.getenv("API_KEY")  # Получаем API ключ из переменных окружения

omdbapi = OMDBApi(API_KEY)  # Инициализируем API OMDB с полученным ключом

current_directory = os.getcwd() # Получаем текущую директорию

file_path_movies = os.path.join(current_directory, 'assets', 'movies.csv') # Путь к файлу movies.csv в папке assets
file_path_distance = os.path.join(current_directory, 'assets', 'distance.csv') # Путь к файлу distance.csv в папке assets

recsys = ContentBaseRecSys(  # Инициализируем систему рекомендаций
    movies_dataset_filepath=file_path_movies,  # Указываем путь к набору фильмов
    distance_filepath=file_path_distance  # Указываем путь к файлу расстояний
)

# Создаем боковую панель
with st.sidebar:
    add_vertical_space(1)  
    img = Image.open("cinema.jpg") 
    st.image(img, width=227) 
st.sidebar.write(
    """ikoskin@yandex.ru  
       @i_koskin"""
)

# Заголовок приложения
st.markdown(
    "<h1 style='text-align: center; color: black;'>Сервис по подбору фильмов</h1>",
    unsafe_allow_html=True
)

# Подзаголовок с информацией о поиске
st.markdown(
    "<h4 style= 'text-align: left; '>Поиск осуществляется по названию фильма, который Вам нравится</h4>",
    unsafe_allow_html=True
)

selected_movie = None  # Инициализируем переменную для выбранного фильма

# Выполняем выбор фильма через селектбокс
movie = recsys.get_titles()
unique_movie = sorted(set(movie)) 

selected_movie = selectbox(
    "Введите или выберите название фильма :",
    unique_movie, # Получаем список названий фильмов
    no_selection_label='---'  # Метка при отсутствии выбора
)

if selected_movie:  
    col1, col2 = st.columns([1, 4]) 
    film_id = recsys.get_film_id(selected_movie)  # Получаем ID выбранного фильма
    with col2:  # В правой колонке отображаем информацию о фильме
        st.markdown("<strong>Выбранный фильм :</strong> " +
                    selected_movie + "<br>" +
                    "<strong>Режиссер :</strong> " +
                    recsys.get_film_directors(film_id) + "<br>" +
                    "<strong>Жанр :</strong> " + ", ".join(recsys.get_film_genres(film_id)) + "<br>" +
                    "<strong>Аннотация :</strong> " + recsys.get_film_overview(film_id),
                    unsafe_allow_html=True)
    with col1:  # В левой колонке отображаем постер фильма
        st.image(omdbapi.get_posters([recsys.get_film_title(film_id)]),
                 use_container_width=True,
                )

st.markdown("""---""")  

# Информация о фильтрах поиска
st.markdown("""По умолчанию поиск ведется по всем категориям.
            Для уточнения Вы можете выбрать <strong>Режиссёра</strong>, <strong>Год</strong> производства или <strong>Жанр</strong> фильма.""", unsafe_allow_html=True)


filter_col = st.columns([1, 1, 1]) 

# Получаем и обрабатываем список режиссеров
with filter_col[0]:  
    directors = recsys.get_list_directors()
    unique_directors = sorted(set(directors))  # Уникальные и отсортированные режиссеры
    selected_director = selectbox(
        "Введите или выберите режиссёра фильма:",
        unique_directors,
        index=0,
        no_selection_label= 'Все режиссёры'
    )

# Получаем и обрабатываем список годов
with filter_col[1]:  
    years = recsys.get_years()
    unique_years = sorted(set(years), reverse=True)  # Уникальные и отсортированные по убыванию годы
    selected_year = selectbox(
        "Введите или выберите год производства фильма:",
        unique_years,
        index=0,
        no_selection_label= 'Все года'
    )

# Получаем и обрабатываем список жанров
with filter_col[2]:  
    genres = recsys.get_genres()
    unique_genres = sorted(set(genres))  # Уникальные и отсортированные жанры
    selected_genre = selectbox(
        "Введите или выберите жанр фильма:",
        unique_genres,
        index=0,
        no_selection_label= 'Все жанры'
    )

# Применяем фильтры, если они выбраны
if selected_director or selected_year or selected_genre:
    recsys.set_filter(selected_director, selected_year, selected_genre)  # Устанавливаем выбранные фильтры
else:
    recsys.remove_filter()  # Убираем фильтры, если ничего не выбрано

if st.button('Показать рекомендации'):  # Проверяем, нажата ли кнопка "Показать рекомендации"
    st.write("Результат подборки:")  # Выводим заголовок для результатов
    if selected_movie:  # Проверяем, выбран ли фильм
        recommended_movie_names = recsys.recommendation(selected_movie, top_k=TOP_K)  # Получаем рекомендованные фильмы
        if len(recommended_movie_names) == 0:  # Если рекомендации пусты
            st.write("К сожалению, рекомендаций не найдено. Измените параметры поиска.")  # Сообщаем об отсутствии рекомендаций
        else:
            titles = [recsys.get_film_title(recsys.get_film_id(name)) for name in recommended_movie_names]  # Получаем названия рекомендованных фильмов
            recommended_movie_posters = omdbapi.get_posters(titles)  # Загружаем постеры рекомендованных фильмов
            
            movies_col = st.columns(TOP_K)  # Создаем колонки для отображения фильмов
            for index in range(min(len(recommended_movie_names), TOP_K)):  # Проходим по рекомендованным фильмам
                with movies_col[index]:  # В каждой колонке
                    st.image(recommended_movie_posters[index], use_container_width=True)  # Отображаем постер фильма
           
            movies_col = st.columns(TOP_K)  # Создаем дополнительные колонки для информации о фильмах
            for index in range(min(len(recommended_movie_names), TOP_K)):  # Проходим по рекомендованным фильмам
                with movies_col[index]:  # В каждой колонке
                    st.markdown("<h5 style='text-align: center;'>" + recommended_movie_names[index] + "</h5",  # Отображаем название фильма
                                unsafe_allow_html=True)
                    rec_id = recsys.get_film_id(recommended_movie_names[index])  # Получаем ID фильма
                    st.markdown(
                        "<p style='text-align: center;'><strong>" +
                        "Год:</strong><br>" +
                        str(recsys.get_film_year(rec_id)) + "<br>" +  # Отображаем год выпуска
                        "<strong>Режиссёр:</strong><br>" + 
                        recsys.get_film_directors(rec_id) + "<br>" +  # Отображаем режиссера
                        "<strong>Жанр:</strong> <br>" +
                        ", ".join(recsys.get_film_genres(rec_id)) + "</p>",  # Отображаем жанры
                        unsafe_allow_html=True)
    else:
        st.write('Извините. Выберите сначала фильм.')  # Если фильм не выбран, выводим сообщение  
