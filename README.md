# «Продуктовый помощник»
[![FoodgramWorkflow](https://github.com/Sovushka-sever/foodgram-project/actions/workflows/foodgram_workflow.yaml/badge.svg)](https://github.com/Sovushka-sever/foodgram-project/actions/workflows/foodgram_workflow.yaml)

Это онлайн-сервис, где пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Инфраструктура

- Проект работает с СУБД PostgreSQL.
- Проект запущен на сервере в Яндекс.Облаке в трёх контейнерах: nginx, PostgreSQL и Django+Gunicorn.
- Контейнер с проектом обновляется на Docker Hub.
- В nginx настроена раздача статики, остальные запросы переадресуются в Gunicorn.
- Данные сохраняются в volumes.

Основной стек: Python 3, Django, PostgreSQL, gunicorn, nginx, Яндекс.Облако(Ubuntu 18.04), Docker

### Предварительные требования
Должны быть установлены Docker и Docker-Compose

Инструкция по установке: 
- [Docker](https://docs.docker.com/get-docker/)
- [Docker-Compose](https://docs.docker.com/compose/install/)

### Установка
Для начала вам нужно склонировать репозиторий и находится в директории yamdb_final:
- Собрать образ
```
docker-compose build
```
- Запустить docker-compose
```
docker-compose up
```
- Для остановки docker-compose
```
docker-compose down

```
## Дополнительные команды
для выполнения этих команд вы должны находится в yamdb_final 
и у вас должен быть запущен docker-compose
- Для выполнения миграций:
```
docker-compose run web python manage.py migrate
```
- Для заполнения базы начальными данными:
```
docker-compose run web python manage.py loaddata fixtures.json
```
- Для создания суперюзера:
```
docker-compose run web python manage.py createsuperuser
```
## Авторы
* **Sovushka-sever** 

## Лицензия
Этот проект находится под лицензией Apache License 2.0. Подробности в файле  [LICENSE](https://github.com/Sovushka-sever/foodgram-project/blob/master/LICENSE)
