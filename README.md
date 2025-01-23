# Recommendation-Service-Cosine-Similarity

Проект "Рекомендательная система выбора фильмов для просмотра"

Цель проекта:
Создание рекомендательной системы, предлагающей пользователю к просмотру фильмы на основе выбора предпочитаемого жанра, продюсера, года релиза

Стек:
• Python (Pandas, Numpy, Scikit-learn, Seaborn, Scipy)
• PostgreSQL, SQLAlchemy
• REST-API
• Git
• Streamlit

В этом проекте реализуем сервис рекомендации фильмов с помощью фреймворка [Streamlit](https://streamlit.io/).

Для построения рекомендательного сервиса фильмов также воспользуемся данными 
[TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata).

Общие данные о фильмах [tmdb_5000_movies](https://files.sberdisk.ru/s/te4QbzdxKgsFQXA).

Каст фильмов [tmdb_5000_credits](https://files.sberdisk.ru/s/H9oRuXQt5mFz3T9).

Этапы работы над проектом
1. Исследование и анализ требований
- Сбор требований: Определение ключевых функций и критериев, по которым будут производиться рекомендации.
- Анализ целевой аудитории: Определение целевой аудитории и ее предпочтений в кино.

2. Сбор данных
- Поиск источников данных: Использование открытых API (TMDb API) для получения информации о фильмах, жанрах, продюсерах и рейтингах.
- Сбор и очистка данных: Сбор данных о фильмах, их жанрах, продюсерах и годах релиза, а также очистка данных от недостоверной информации и дубликатов.

3. Предварительная обработка данных
- Обработка пропусков: Замена или удаление пропущенных значений в данных.
- Кодирование категориальных данных: Преобразование текстовых данных (жанры, продюсеры) в числовые форматы с использованием One-Hot Encoding.
- Нормализация данных: Приведение числовых данных к единому масштабу.

4. Создание модели рекомендаций
- Выбор алгоритма: Определение методов рекомендательной системы (Content-Based Filtering).
- Реализация выбранного алгоритма (Cosine Similarity) для выдачи рекомендаций.

5. Разработка интерфейса
- Разработка фронтенда: Проектирование и создание пользовательского интерфейса с использованием инструментов Streamlit.
- Интеграция с бэкендом: Связывание фронтенда с серверной частью через RESTful API.

6. Разработка бэкенда
- Выбор технологий: Использование Python для разработки серверной части.
- Создание API: Разработка RESTful API (OMDB API) для обработки запросов пользователей и выдачи рекомендаций.
