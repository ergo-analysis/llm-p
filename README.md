## Инструкция по запуску:

### Установка окружения и пакетов

Установить пакетный менеджер uv: 
```pip install uv```

В корне проекта инициализировать uv: 
```uv init```

Создать виртуальное окружение: 
```uv venv```
 
Активировать виртуальное окружение: 
```source .venv/bin/activate``` 

или Windows:
```.venv\Scripts\activate.bat```

Установить зависимости:  
```uv pip install -r <(uv pip compile pyproject.toml)```

### Настройка .env 
Создать .env файл (см. шаблон env.example)

Зарегистрироваться и получить ключ на сайте: https://openrouter.ai

Добавить ключ в .env в переменную 
```OPENROUTER_API_KEY```

### Запуск и работа
Запустить проект: 
```uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000```

Перейти по ссылке: http://0.0.0.0:8000/docs

Для выполнения сценариев раскрывать строку эндпоинта и нажимать try out
 
## Примеры работы: 

Общий экран swagger:

![alt text](screenshots/общий_вид.PNG)

Регистрация: 

![alt text](screenshots/регистрация.PNG)

Логин и получение JWT:

![alt text](screenshots/логин.PNG)

OAuth авторизация:

![alt text](screenshots/OAuth_логин.PNG)

Вызов POST /chat:

![alt text](screenshots/первое_сообщение.PNG)

![alt text](screenshots/второе_сообщение.PNG)

Вызов GET /chat/history:

![alt text](screenshots/история_диалога.PNG)

Вызов DELETE /chat/history:

![alt text](screenshots/удаление_истории.PNG)

![alt text](screenshots/пустая_история.PNG)

Вызов GET /health:

![alt text](screenshots/здоровье.PNG)

## Обработка специфичных сценарииев

**Защищённые эндпоинты недоступны без токена**

![alt text](screenshots/extra_cases/неавторизован.PNG)

**Данные разных пользователей не смешиваются**

Логиним тестового юзера
![alt text](screenshots/extra_cases/тестовый_юзер.PNG)

У тестового юзера есть свой диалог
![alt text](screenshots/extra_cases/история_тестового_юзера.PNG)

Логиним исходного юзера
![alt text](screenshots/extra_cases/другой_юзер.PNG)

Исходный юзер имеет свою раннее очищенную историю и не подтягивает чужие сообщения
![alt text](screenshots/extra_cases/история_не_смешивается.PNG)
