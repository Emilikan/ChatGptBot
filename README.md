# Чат бот для Telegram на основе бесплатной gpt4

Для запуска:
1) Добавить в проект в папку deploy файл с именем ```.env``` следующего содежания
   ```bash
   # Base
   PROJECT_NAME           = chat_gpt
   LOGGING_CONFIG_PATH    = app/config/logging.ini
   CHAT_GPT_MODEL         = gpt-4
   MAIN_ADMIN             = YOUR_MAIN_ADMIN_TG_ID # ID главного администратора (численное значение типа 123456789, можно получить, например, с    помощью бота https://t.me/getmyid_bot)
   ADMINS                 = [YOUR_ADMIN_ID_1, YOUR_ADMIN_ID_2] # id администраторов
   REQUEST_LIMIT          = 40
   CONTEXT_MESSAGE_LIMIT  = 200

   # Telegram BOT
   MAIN_ADMIN             = YOUR_MAIN_ADMIN_TG_ID
   TG_OWNER_ID            = YOUR_MAIN_ADMIN_TG_ID
   TG_BOT_TOKEN           = YOUR_TG_BOT_TOKEN # Токен вашего бота - можно получить в https://t.me/BotFather при создании бота
   THROTTLING_RATE        = 0.5
   TG_API_URL             = https://api.telegram.org
   REDIS_USE              = true

   #Webhook
   WEBHOOK_PORT = 1234
   WEBHOOK_URL = 
   WEBHOOK_PATH = /webhook
   DROP_PENDING_UPDATES = false
   WEBHOOK_USE = false

   # PostgreSQL
   POSTGRES_USER          = postgres
   POSTGRES_PASSWORD      = 1234
   POSTGRES_HOST          = db
   POSTGRES_HOST_PORT     = 5433
   POSTGRES_PORT          = 5432
   POSTGRES_DB            = chat_gpt

   # Redis
   REDIS_HOST             = redis
   REDIS_HOST_PORT        = 6380
   REDIS_PORT             = 6379
   REDIS_DB               = 0
   ```
2) Сбилдить проект в докер образ
   ```bash
   make compose-build
   ```
4) Запустить докер образ
   ```bash
   make compose-up
   ```
