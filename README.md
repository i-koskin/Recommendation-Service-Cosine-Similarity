## 🎬 Рекомендательная система выбора фильмов

### Цель проекта

Разработка рекомендательной системы, предлагающей пользователю фильмы для просмотра на основе:

- предпочитаемого жанра,
- режиссёра,
- года релиза.

---

### 🛠 Используемые технологии

- [Streamlit](https://streamlit.io/) — веб-фреймворк для интерактивных приложений на Python
- [OMDb API](https://www.omdbapi.com/) — API для получения информации о фильмах
- Датасет [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)

---

### 🚀 Быстрый старт

### 1. Установка зависимостей

Установите необходимые библиотеки:

```bash
pip install streamlit
pip install streamlit-extras
```
### 2. Клонирование репозитория

Скачайте репозиторий в локальную директорию:

```bash
git clone https://github.com/i-koskin/Recommendation-Service-Cosine-Similarity.git
cd Recommendation-Service-Cosine-Similarity
```

### 2. Скачивание и подготовка данных

Скачайте и поместите в папку `./Recommendation_Service` следующие файлы:

- [tmdb_5000_movies.csv](https://files.sberdisk.ru/s/te4QbzdxKgsFQXA) — общая информация о фильмах
- [tmdb_5000_credits.csv](https://files.sberdisk.ru/s/H9oRuXQt5mFz3T9) — информация о касте фильмов

### 3. Подготовка данных

Откройте и выполните все ячейки ноутбука `distances.ipynb`, расположенного по пути:

```
./Recommendation_Service/src/notebooks/distances.ipynb
```

### 4. Настройка переменных окружения

Создайте файл `.env` в папке `./Recommendation_Service/src` с содержимым:

```
API_KEY=ваш_ключ_OMDb
```

> Получите `API_KEY` на сайте [OMDb API](https://www.omdbapi.com/apikey.aspx)

### 5. Запуск приложения

В терминале:

```bash
cd ./Recommendation_Service/src
streamlit run app.py
```

---

### 🎥 Как пользоваться

1. Введите или выберите фильм, который вам нравится.
2. Нажмите кнопку **"Показать рекомендации"**.
3. Для более точного результата можно указать:
   - Режиссёра
   - Год выпуска
   - Жанр

По умолчанию поиск производится по всем категориям.

---

### 📸 Пример работы рекомендательной системы

<p align="center">
<img src="Recommendation_Service/src/docs/rec_sys.JPG" width="400">
</p>

---
