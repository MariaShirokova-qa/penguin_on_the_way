# Руководство по деплою на PythonAnywhere

## Шаг 1: Регистрация на PythonAnywhere

1. Перейдите на https://www.pythonanywhere.com/
2. Зарегистрируйтесь (выберите бесплатный тариф "Beginner")
3. Подтвердите email

## Шаг 2: Создание нового Web App

1. Зайдите в "Web" tab
2. Нажмите "Add a new web app"
3. Выберите "Manual configuration" (не Django!)
4. Выберите Python 3.10 или новее
5. Нажмите "Next"

## Шаг 3: Загрузка кода проекта

### Вариант A: Через Git (рекомендуется)

1. Создайте репозиторий на GitHub
2. Загрузите код проекта:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/gym_app.git
   git push -u origin main
   ```

3. На PythonAnywhere в консоли:
   ```bash
   git clone https://github.com/yourusername/gym_app.git
   cd gym_app
   ```

### Вариант B: Через Drag-and-drop

1. В PythonAnywhere откройте Files
2. Загрузите папку проекта (без venv)
3. Распакуйте архив

## Шаг 4: Настройка виртуального окружения

1. В PythonAnywhere консоли:
   ```bash
   cd ~/gym_app
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## Шаг 5: Настройка базы данных

PythonAnywhere использует PostgreSQL вместо SQLite:

1. В PythonAnywhere перейдите в "Databases" tab
2. Создайте новую базу данных (PostgreSQL)
3. Запишите данные подключения:
   - Database name
   - Username
   - Password
   - Host
   - Port

4. Обновите settings.py:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_db_name',
           'USER': 'your_db_user',
           'PASSWORD': 'your_db_password',
           'HOST': 'your_db_host',
           'PORT': 'your_db_port',
       }
   }
   ```

5. Запустите миграции:
   ```bash
   python manage.py migrate
   ```

6. Создайте суперпользователя:
   ```bash
   python manage.py createsuperuser
   ```

## Шаг 6: Сбор статических файлов

1. В консоли PythonAnywhere:
   ```bash
   python manage.py collectstatic
   ```

## Шаг 7: Настройка WSGI файла

1. В PythonAnywhere перейдите в "Web" tab
2. Нажмите на "WSGI configuration file"
3. Замените содержимое на:

```python
import os
import sys

path = '/home/yourusername/gym_app'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'gym_project.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

4. Замените `yourusername` на ваш логин PythonAnywhere

## Шаг 8: Настройка Web App

1. В "Web" tab:
   - **Code directory**: `/home/yourusername/gym_app`
   - **Virtualenv**: `/home/yourusername/gym_app/venv`
   - **WSGI file**: `/home/yourusername/gym_app/gym_project/wsgi.py`

2. В "Static files" section:
   - URL: `/static/`
   - Directory: `/home/yourusername/gym_app/staticfiles`

3. Нажмите "Reload" для перезагрузки

## Шаг 9: Настройка SECRET_KEY

1. В PythonAnywhere создайте переменную окружения:
   - Перейдите в "Web" tab → "Variables"
   - Добавьте: `DJANGO_SECRET_KEY` (сгенерируйте новый ключ)
   - В settings.py замените на:
     ```python
     import os
     SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'your-dev-key')
     ```

## Шаг 10: Проверка

1. Откройте ваш сайт: `https://yourusername.pythonanywhere.com/`
2. Проверьте, что все работает
3. Попробуйте зайти в админку: `/admin/`

## Дополнительные настройки

### Отключение DEBUG в продакшене

В settings.py:
```python
DEBUG = False
```

### Настройка ALLOWED_HOSTS

Замените на ваш домен:
```python
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']
```

## Возможные проблемы

### Ошибка "ModuleNotFoundError"
- Убедитесь, что все зависимости установлены: `pip install -r requirements.txt`

### Ошибка с базой данных
- Проверьте данные подключения к PostgreSQL
- Запустите миграции: `python manage.py migrate`

### Статические файлы не загружаются
- Запустите `python manage.py collectstatic`
- Проверьте путь к staticfiles в настройках Web App

### 502 Bad Gateway
- Проверьте логи в "Web" tab → "Log files"
- Убедитесь, что WSGI файл настроен правильно
