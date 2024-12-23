Телеграм-бот для бронирования
	Этот телеграм-бот предназначен для упрощения процесса бронирования времени. 

Функциональность
	Бот позволяет:
	* Посмотреть список всех врачей (Рис. 2)
	* Посмотреть список услуг (Рис. 3)
	* Посмотреть отзывы (Рис. 4)
	* Записаться на прием, выбрав врача, услугу, дату и время (информация о бронировании сохраняется в БД) (Рис. 5)

Технологии 
	*  Python-telegram-bot
	*  SQLite
	
Использование
	1.  **Клонирование репозитория:**
    	```bash
    	git clone https://github.com/DDos28/bot
    	cd <имя_вашей_папки>
    	```
	2.  **Заполнение токена:** Откройте файл `main.py` и замените строку `""` на токен вашего бота.
    	```python
    	updater = Updater("Ваш_токен")
    	```
	3.  **Запуск бота:** Запустите файл `main.py` с помощью Python:
    	```bash
    	python main.py
    	```
	4.  **Использование бота:** Откройте Telegram и найдите вашего бота. Начните взаимодействие с помощью команды `/start`.

Требования
	1.  **Python 3.6+:** Убедитесь, что у вас установлен Python версии 3.6 или выше.
	2.  **Python-telegram-bot:** Установите библиотеку python-telegram-bot, используя `pip`:
    	```bash
    	pip install python-telegram-bot
    	```
	3.  **Токен Telegram бота:** Получите токен своего бота у @BotFather в Telegram.

Данный проект был разработан с целью:
	1.  **Практическое применение:** Демонстрация навыков работы с Telegram Bot API и создания интерактивного бота.
	2.  **Упрощение бронирования:** Предоставление удобного инструмента для бронирования времени через Telegram.
	3.  **Изучение ConversationHandler:** Освоение работы с `ConversationHandler` для управления диалогами с пользователем.
	4.  **Обучение работе с базами данных:** Использование SQLite для хранения и управления данными бронирований.

Структура проекта

	*   `main.py`: Основной файл с логикой бота.
	*   `database.py`: Файл с кодом для подключения к базе данных.
	*   `crud_function.py`: Файл с кодом для создания таблиц и добавления данных в базу.
	*   `telegram.db`: Файл базы данных SQLite (создается при первом запуске).

Автор
Кирилл Ершов
[DDos28](https://github.com/DDos28)

Рис. 1
![Рис  1](https://github.com/user-attachments/assets/168c433d-9798-40f7-8928-0da8ce9778c6)

Рис. 2
![Рис  2](https://github.com/user-attachments/assets/36d3b035-5fcc-44b5-ae6b-9a692cb78263)

Рис. 3
![Рис  3](https://github.com/user-attachments/assets/ca05095f-b6b2-4d04-bd8a-9fe3c6159157)

Рис. 4
![Рис  4](https://github.com/user-attachments/assets/96a26b6e-8fa1-4b2a-9c26-c0cf3e230168)

Рис. 5
![Рис  5](https://github.com/user-attachments/assets/ce990c9d-2e33-4812-8fb9-07033fdbc5dc)
