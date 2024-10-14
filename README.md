# Weather Bot

Этот проект представляет собой бота для Telegram, который предоставляет информацию о погоде в различных городах. Бот использует OpenWeatherMap API для получения данных о погоде и реализован на Python с использованием библиотеки `pyTelegramBotAPI`.

## Стек технологий

- Python 3.10
- Docker
- OpenWeatherMap API

## Установка

Для запуска проекта потребуется Docker и Docker Compose. Следуйте этим шагам:

### 1. Клонирование репозитория

```bash
git clone https://github.com/trixvlq/WeatherBot
cd WeatherBot
```

2. Настройка окружения

Создайте файл .env в корневой директории проекта и добавьте ваши токены:
```bash
BOT_TOKEN='7572524642:AAFkVVX61kbFzd0jJtQtnDRrZAg6sAI7DUw'
API_KEY='cb8801fceffebeb18636363fc0e20105'
```

3. Сборка контейнера
Используйте Docker Compose для сборки и запуска контейнера:

``` bash
docker-compose up --build
```
4. Запуск бота

После сборки и запуска контейнера бот начнет работать и будет готов к приему команд в Telegram по ссылке https://t.me/NotSoUniqueWeatherBot.

Использование


Запустите бота в Telegram, отправив команду /start для приветствия.

Используйте команду /weather [Название города] для получения информации о погоде в выбранном городе.

Для получения списка доступных команд используйте /help.

Примечания


Убедитесь, что ваши токены корректны, иначе бот не сможет получить доступ к API.

Контакты

gmail:qwefghnz@gmail.com

githun:https://github.com/trixvlq

telegram:@tszyuo
