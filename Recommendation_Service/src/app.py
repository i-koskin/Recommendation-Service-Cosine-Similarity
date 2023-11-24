import os

import streamlit as st
from streamlit_extras.no_default_selectbox import selectbox
from streamlit_extras.add_vertical_space import add_vertical_space

from dotenv import load_dotenv

from PIL import Image
from api.omdb import OMDBApi
from recsys import ContentBaseRecSys

TOP_K = 5
load_dotenv()

API_KEY = os.getenv("API_KEY")
MOVIES = os.getenv("MOVIES")
DISTANCE = os.getenv("DISTANCE")

omdbapi = OMDBApi(API_KEY)

recsys = ContentBaseRecSys(
    movies_dataset_filepath=MOVIES,
    distance_filepath=DISTANCE,
)



with st.sidebar:
    add_vertical_space(1)
    img = Image.open ("cinema.jpg")
    st.image (img, width=227)
st.sidebar.write(
    """kombucha@student.21-school.ru  
    Intensive Parallel  
    21 TGU_DS_0423  
    Tribe: Venus  
    26.04.2023 - 08.08.2023"""
)

st.markdown(
    "<h1 style='text-align: center; color: black;'>Сервис по подбору фильмов</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<h4 style= 'text-align: left; '>Поиск осуществляется по названию фильма, который Вам нравится</h4>",
    unsafe_allow_html= True
)

selected_movie= None

selected_movie = selectbox(
    "Введите или выберите название фильма :",
    recsys.get_titles(),
    no_selection_label= '---'
)

if selected_movie:
    col1, col2 = st.columns([1, 4])
    film_id = recsys.get_film_id(selected_movie)
    with col2:
        st.markdown("**Выбранный фильм** : " +
                    selected_movie + "<br>" + 
                    "**Режиссер** : " +
                    recsys.get_film_directors(film_id) + "<br>" +
                    "**Жанр** : " + ", ".join(recsys.get_film_genres(film_id)) + "<br>" +
                    "**Аннотация** : " + recsys.get_film_overview(film_id),
                    unsafe_allow_html= True)
    with col1:
        st.image(omdbapi.get_posters([recsys.get_film_title(film_id)]),
                 use_column_width= True)

st.markdown("""---""")

st.markdown("""По умолчанию поиск ведется по всем фильмам.
            Для ускорения поиска Вы можете выбрать <strong>Режиссёра</strong>, <strong>Год</strong> производства или <strong>Жанр</strong> фильма.""", unsafe_allow_html= True)

filter_col = st.columns([1, 1, 1])

with filter_col[0]:
    selected_director = selectbox(
        "Введите или выберите режиссёра фильма:",
        recsys.get_list_directors(),
        no_selection_label= 'Все режиссёры'
        )
with filter_col[1]:
    selected_year = selectbox(
        "Введите или выберите год производства фильма:",
        recsys.get_years(),
        no_selection_label= 'Все года'
    )
with filter_col[2]:
    selected_genre = selectbox(
        "Введите или выберите жанр фильма:",
        recsys.get_genres(),
        no_selection_label= 'Все жанры'
    )

if selected_director or selected_year or selected_genre:
    recsys.set_filter(selected_director, selected_year, selected_genre)
else:
    recsys.remove_filter()
      

if st.button('Показать рекомендации'):
    st.write("Результат подборки:")
    if selected_movie:
        recommended_movie_names = recsys.recommendation(selected_movie, top_k= TOP_K)
        if len(recommended_movie_names) == 0:
            st.write("К сожалению, рекомендаций не найдено. Измените параметры поиска.")
        else:
            titles = [recsys.get_film_title(recsys.get_film_id(name)) for name in recommended_movie_names]
            recommended_movie_posters = omdbapi.get_posters(titles)
            
            movies_col = st.columns(TOP_K)
            for index in range(min(len(recommended_movie_names), TOP_K)):
                with movies_col[index]:
                    st.image(recommended_movie_posters[index],
                            use_column_width= True)
           
            movies_col = st.columns(TOP_K)
            for index in range(min(len(recommended_movie_names), TOP_K)):
                with movies_col[index]:
                    st.markdown("<h5 style='text-align: center;'>" + recommended_movie_names[index] + "</h5",
                                unsafe_allow_html= True)
                    rec_id = recsys.get_film_id(recommended_movie_names[index])
                    st.markdown(
                        "<p style='text-align: center;'><strong>" +
                        "Год:</strong><br>" +
                        str(recsys.get_film_year(rec_id)) + "<br>" +
                        "<strong>Режиссёр:</strong><br>" + 
                        recsys.get_film_directors(rec_id) + "<br>" +
                        "<strong>Жанр:</strong> <br>" +
                        ", ".join(recsys.get_film_genres(rec_id)) + "</p>",
                        unsafe_allow_html= True)
    else:
        st.write('Извините. Выберите сначала фильм.')      
