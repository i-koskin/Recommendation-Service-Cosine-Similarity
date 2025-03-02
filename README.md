## Проект "Рекомендательная система выбора фильмов для просмотра"


### Цель проекта:
Создание рекомендательной системы, предлагающей пользователю к просмотру фильмы на основе выбора предпочитаемого жанра, режиссёра, года релиза.

### Порядок работы с рекомендательной системой:

В этом проекте реализуем сервис рекомендации фильмов с помощью фреймворка [Streamlit](https://streamlit.io/).

pip install streamlit

pip install streamlit-extras

#### 1. Скачайте репозиторий в локальную папку
Для построения рекомендательного сервиса фильмов воспользуемся данными [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata).
#### 2. Скачайте и переместите в папку /Recommendation_Service:
2.1. Общие данные о фильмах [tmdb_5000_movies](https://files.sberdisk.ru/s/te4QbzdxKgsFQXA).

2.2. Каст фильмов [tmdb_5000_credits](https://files.sberdisk.ru/s/H9oRuXQt5mFz3T9).
#### 3. Для подготовки данных запустите на выполнение все ячейки в файле distances.ipynb

Файл distances.ipynb находится  в папке /Recommendation_Service/src/notebooks
#### 4. Создайте и сохраните файл .env:
- в любом текстовом редакторе создайте файл с назанием .env
- в фале .env укажите API_KEY = '*'

  (вместо * вставьте API_KEY, полученный на сайте [OMDb API](https://www.omdbapi.com) для доступа к RESTful веб-сервису для получения информации о фильмах)
- файл .env сохраните в папке /Recommendation_Service/src
#### 5. В терминале:
- перейдите в папку /Recommendation_Service/src;
- streamlit run app.py
#### 6. Получение рекомендаций
- Введите или выберите название фильма, который Вам нравится и на основании которого Вы бы хотели получить рекомендации;
- Нажмите кнопку "Показать рекомендации".

  По умолчанию поиск ведется по всем категориям. Для уточнения Вы можете выбрать Режиссёра, Год производства или Жанр фильма.
