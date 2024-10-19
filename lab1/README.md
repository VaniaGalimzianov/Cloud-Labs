# Лабораторная работа №1

## Цель
Цель первой лабораторной работы - настроить nginx на локальном сервере.

Подробнее:
1. Должен работать по https c сертификатом
2. Настроить принудительное перенаправление HTTP-запросов (порт 80) на HTTPS (порт 443) для обеспечения безопасного соединения
3. Использовать alias для создания псевдонимов путей к файлам или каталогам на сервере
4. Настроить виртуальные хосты для обслуживания нескольких доменных имен на одном сервере

## Первый шаг
Для начала, создадим два любых проекта. В нашем случае - два проекта на `FastAPI`, которые на "главной странице" возвращают `json` с именем проекта. Первый будем поднимать на `8000` порту, а второй на `8001`.

## Второй шаг
Устанавливаем `nginx`. Потом в `/etc/nginx/sites-available/server` пропишем перенаправление с `http` на `https` для `project1.localhost` и `project1.localhost`:

![image](https://github.com/user-attachments/assets/bf5a2bf5-790b-4f4d-aa80-5df24cb81492)

## Третий шаг
Создадим самоподписанные SSL-сертификаты для подключения по `https` командой `sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/<name>.key -out /etc/ssl/certs/<name>.crt` 

Для первого проекта:

![image](https://github.com/user-attachments/assets/9586416e-c3fa-4e33-8375-8643b1421f4e)

И для второго:

![image](https://github.com/user-attachments/assets/89f05295-6e9c-4607-b063-395c9165cd96)

## Четвертый шаг

Теперь можно продолжить настраивать конфиг `nginx`, в `location` указывая созданные сертификаты и что, при попадании на `/`, перенаправляем на `127.0.0.1:port`

![image](https://github.com/user-attachments/assets/3abe9a3c-2ea7-44f7-b341-282794b5de79)

И создадим символическую ссылка на наш файл командой `sudo ln -s /etc/nginx/sites-available/server /etc/nginx/sites-enabled/`

P.S. было бы хорошо разбить на 2 файла конфиги для каждого домена. Тогда пришлось бы симовлическую ссылку создавать для каждого из них.

### Проверка работоспособности
`sudo nginx -t` - этой командой проверим, не допустили ли мы нигде ошибку. После чего перезапустим `nginx` командой `sudo systemctl restart nginx`. Зайдем на `http://project1.localhost/` и `http://project2.localhost/`:

![image](https://github.com/user-attachments/assets/9d9756bc-78ea-4cc9-9709-20522671f66b) ![image](https://github.com/user-attachments/assets/cd114376-b7b2-44f6-8727-0fab5003b39b)

Всё работает

## Пятый шаг
Настроим alias так, чтобы во втором проекте при переходе на `img`, можно было посмотреть рис по-Тайски. Да еще и так, чтобы `FastAPI` в этом не был задействован. Для этого в конфиге пропишем `alias` для `/img/`:

![image](https://github.com/user-attachments/assets/d6b808df-33da-4b16-a485-6fa1c277fd20)

### Результат
![image](https://github.com/user-attachments/assets/f7ea126e-49ec-4966-bd7a-4ffc072cfe2b)

![image](https://github.com/user-attachments/assets/6e18b2d1-75ac-4c62-a41c-f137a40fe9b3)

## Заключение
У нас есть два проекта на одном сервере. Оба доступны по https. Веб сервер перенаправляет на нужный проект и переопределяет путь для фотографий.
