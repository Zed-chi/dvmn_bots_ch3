# Два бота с интеграцией dialogflow

Реализация ответов бота с помощью google dialogflow

### Требования:

- python 3.8
- Создать телеграм бот, получить токен от него
- Создать сообщество ВК, получить api ключ, включить longpooling
- Как создать проект в [dialogflow](https://cloud.google.com/dialogflow/docs/quick/setup)
- Создать агент в [dialogflow](https://cloud.google.com/dialogflow/docs/quick/build-agent)
- Включить API DialogFlow на вашем Google-аккаунте

### Установка:

- `pip install -r requirements.txt`
- в корне проекта создать файл .env и прописать значения:

```
TG_BOT_TOKEN=<Токен от ТГ бота>
TG_BOT_NAME=<Имя ТГ бота>
GOOGLE_CLOUD_PROJECT=<ID Проекта dialogflow>
PROJECT_SUFFIX=<Имя Проекта dialogflow>
PROJECT_API_KEY=<Ключ dialogflow полученный с помощью googlecli>
GOOGLE_APPLICATION_CREDENTIALS=<путь до файла с ключами от Google, credentials.json>
VK_GROUP_TOKEN=<Токен от группы ВК>
VK_GROUP_ID=<Номер группы ВК>
LOG_LEVEL=<Уровень логирования - DEBUG/INFO/WARNING>
```

### Обучение DialogFlow/Наполнение Intent-ов:

- Скачать файл [questions.json](https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json), поместить в корень проектов.
- Выполнить команду `python teach_dialogflow_from_json.py`

### Запуск:

- Запуск тг бота - `python tg_bot.py`.
- Запуск вк бота - `python vk_bot.py`.

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
