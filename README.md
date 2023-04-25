# Shopping_pathfinding

## Требования

* Docker Compose. [Установка](https://docs.docker.com/compose/install/)
* Наличие ключа API Яндекс Карт. Для получения ключа выполните [шаг 1](https://yandex.ru/dev/maps/jsapi/doc/2.1/quick-start/index.html)

## Подключение API 
Создайте в директории `/client/src` файл с названием `conf.js` и добавьте в него строчку с вашим API-ключом:

`export const api_key = 'ваш API-ключ'`

## Сборка докер образов

`docker-compose build`

## Запуск контейнеров

`docker-compose up`

Это приложение доступно на `http://localhost:3000`
