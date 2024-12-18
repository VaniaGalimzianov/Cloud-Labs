# Лабораторная работа №2 со звездочкой: Docker-compose
Цель второй лабораторной работы со звездочкой - ознакомление с принципами написания `Docker-compose` файла. Будут 
рассмотрены плохие практики написания файла, а затем они будут исправлены. Кроме того, будет настроен файл так, чтобы 
контейнеры поднимались вместе, но не видели друг друга по сети.


## Подготовка
За основу возьмем два проекта из первой лабораторной работы - два примитивных сайта на `Python`. В каждом из проектов 
создадим `Dockerfile` с одинаковым содержимым: 

```
FROM python:3.11-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml ./

RUN poetry lock

RUN poetry install --no-dev

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Теперь можно написать плохой `Docker-compose` файл и разобрать допущенные ошибки.

В папке, содержащей два проекта, создадим `docker-compose.yml` со следующим содержанием:

```
version: '3.8'

services:
  first_project:
    build:
      context: ./first_project
      dockerfile: Dockerfile
    container_name: first_project
    ports:
      - "8001:8000"
    environment:
      - TOKEN=156sdflkwf5645

  second_project:
    build:
      context: ./second_project
      dockerfile: Dockerfile
    container_name: second_project
    ports:
      - "8002:8000"
```

## 1st bad practice
Первая ошибка - задали явное имя контейнера:
```
container_name: <project_name>
```
Да, это может быть моментами удобно, однако это также приводит и к ошибкам при 
запуске нескольких экземпляров проекта.
### Исправления
Стоит убрать эти строки из compose-файла.
## 2nd bad practice
Мы в `first_project` задали значение переменной `TOKEN` прямо в compose-файле: 
```
environment:
  - TOKEN=156sdflkwf5645
```
Это нарушает принципы разделения конфигурации и кода.
### Исправления
Стоит вынести это в отдельный файл `.env`:
```
TOKEN=156sdflkwf5645
```
а в compose-файле заменить на:
```
environment:
  - TOKEN=${TOKEN}
```
## 3rd bad practice

Следующей ошибкой является не указание локального интерфейса при указании портов:
```
ports:
  - "<port>:8000"
```
В этом случае порт будет привязан ко всем доступным интерфейсам. Следовательно, в продакшене это может привести к доступу
из внешней сети.
### Исправления
Для того, чтобы это исправить, стоит указать локальный интерфейс:
```
ports:
  - "127.0.0.1:<port>:8000"
```
## Изоляция сервисов
Мы каждый сервис подключим к собственной сети: `first_project_network` и `second_project_network` соответственно. Получим такой compose-файл:
```
version: '3.8'

services:
  first_project:
    build:
      context: ./first_project
      dockerfile: Dockerfile
    ports:
      - "127.0.0.1:8001:8000"
    environment:
      - TOKEN=${TOKEN}
    networks:
      - first_project_network

  second_project:
    build:
      context: ./second_project
      dockerfile: Dockerfile
    ports:
      - "127.0.0.1:8002:8000"
    networks:
      - second_project_network

networks:
  first_project_network:
  second_project_network:
```
Проверим:

![image](https://github.com/user-attachments/assets/545fd454-67b2-43e4-99bb-e559698a8139)

Сайты работают. Проверим их изолированность:

![image](https://github.com/user-attachments/assets/37404639-4f80-4b6a-b4bc-022395a46eaa)

Т.к. сервисы в `Docker-compose` в одной сети могут общаться, а в разных - нет, то этим мы добились требуемой изоляции.

## Заключение
У нас есть два проекта, у каждого есть свой `Dockerfile`. Всё собрано в `Docker-compose`. Доступны они только в локальной сети, переменные окружения хранятся в `.env`, без проблем можем создавать несколько экземпляров проекта. А также добились изоляции контейнеров друг от друга.

И мем:

![image](https://github.com/user-attachments/assets/6abe95e6-80e2-4be6-b7c7-27ca0d426ac4)
