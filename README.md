# Два бота с интеграцией dialogflow

Реализация ответов бота с помощью google dialogflow.
Dialogflow — это платформа для понимания естественного языка, используемая для разработки и интеграции диалогового пользовательского интерфейса в мобильные приложения, веб-приложения, устройства, боты, интерактивные системы голосового ответа и связанные с ними приложения.
Сервис дает возможность обучения на диалогах.

Пример работы:

![image info](https://dvmn.org/filer/canonical/1569214094/323/)
![image info](https://dvmn.org/filer/canonical/1569214089/322/)

### Требования:

- python 3.8
- Создать телеграм бот, получить токен от него
- Создать сообщество ВК, получить api ключ, включить longpooling
- Как создать проект в [dialogflow](https://cloud.google.com/dialogflow/docs/quick/setup)
- Создать агент в [dialogflow](https://cloud.google.com/dialogflow/docs/quick/build-agent)
- [Включить API DialogFlow](https://cloud.google.com/dialogflow/es/docs/quick/setup#api) на вашем Google-аккаунте
- Получить ключи credentials.json c помощью [google cli](https://cloud.google.com/dialogflow/es/docs/quick/setup#sdk)
- [Создать токен](https://cloud.google.com/docs/authentication/api-keys) DialogFlow

### Установка:

- `pip install -r requirements.txt`
- в корне проекта создать файл .env и прописать значения:

```
TG_BOT_TOKEN=<Токен от ТГ бота>
TG_BOT_NAME=<Имя ТГ бота>
TG_ADMIN_CHAT_ID=<id tg разработчика для отсылки сообщений с ошибками >

VK_GROUP_TOKEN=<Токен от группы ВК>
VK_GROUP_ID=<Номер группы ВК>

PROJECT_SUFFIX=<Имя Проекта dialogflow>
GOOGLE_APPLICATION_CREDENTIALS=<путь до файла с ключами от Google, credentials.json>
GOOGLE_CLOUD_PROJECT=<ID Проекта dialogflow>
PROJECT_API_KEY=<токен полученный с помощью google cli>
LOG_LEVEL=<Уровень логирования - DEBUG/INFO/WARNING>
LOG_PATH=<Путь к лог файлу>
LOGGER_TYPE=<Вариант вывода лога FILE/TG> либо вывод в консоль при отсутствии
```

### Обучение DialogFlow/Наполнение Intent-ов:

- Скачать файл [questions.json](https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json), поместить в корень проектов.
- Выполнить команду `python teach_dialogflow_from_json.py`
- `-p` аргумент пути до файла с данными для обучения, по-умолчанию это `./questions.json`

### Запуск:

- Запуск тг бота - `python tg_bot.py`.
- Запуск вк бота - `python vk_bot.py`.

  Тестовые версии:

- https://vk.com/club131455573
- https://t.me/zedchi_dialog_bot

### Перенос на Linux сервер:

Для запуска на сервере нужно:

- Разархивировать проект либо клонировать из github
- Запомнить путь где лежит архив
- Создать systemd сервисы для фонового запуска при старте системы
- В папке systemd_services есть примеры `.service` файлов, нужно только изменить путь в котором лежит проект.
- После нужно решить какой вариант запуска будете использовать (ВК/ТГ/Оба)
- включаете сервис `systemctl enable <нащвание сервис файла>`
- запускаете сервис - `systemctl start myunit`

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
