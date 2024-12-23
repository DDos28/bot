import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, ConversationHandler
from telegram import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
import database

CHOOSING_DOCTOR = 1
CHOOSING_SERVICE = 2
CHOOSING_DATE_TIME = 3
CONFIRMATION = 4

BOT_TOKEN = ''

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляет пользователю сообщение “Выберите действие:” с клавиатурой главного меню."""
    reply_markup = create_main_menu_keyboard()
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Выберите действие:",
                                   reply_markup=reply_markup)


def create_main_menu_keyboard():
    """Создает клавиатуру главного меню."""
    button_doctors = InlineKeyboardButton("Список врачей", callback_data='doctors')
    button_services = InlineKeyboardButton("Список услуг", callback_data='services')
    button_appointment = InlineKeyboardButton("Записаться на прием", callback_data='appointment')
    button_reviews = InlineKeyboardButton("Отзывы", callback_data='reviews')

    keyboard = [
        [button_doctors],
        [button_services],
        [button_appointment],
        [button_reviews]
    ]
    return InlineKeyboardMarkup(keyboard)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает нажатия кнопок, полученные от пользователя."""
    query = update.callback_query
    await query.answer()
    if query.data == 'doctors':
        doctors = database.get_doctors()
        text = "Список врачей:\n"
        for doctor in doctors:
            text += f"- {doctor[1]} ({doctor[2]})\n"
        await query.edit_message_text(text=text)
    elif query.data == 'services':
        services = database.get_services()
        text = "Список услуг:\n"
        for service in services:
            text += f"- {service[1]} - {service[2]} руб. ({service[3]})\n"
        await query.edit_message_text(text=text)
    elif query.data == 'reviews':
        reviews = database.get_reviews()
        text = "Отзывы:\n"
        for review in reviews:
            text += f"- {review[0]} ({review[1]} звезд)\n"
        await query.edit_message_text(text=text)


async def choose_doctor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Извлекает список врачей из базы данных, формирует Inline-клавиатуру с кнопками, каждая из которых
    представляет врача, и отправляет сообщение пользователю с просьбой выбрать врача, устанавливая состояние диалога
    CHOOSING_DOCTOR."""
    doctors = database.get_doctors()
    keyboard = []
    for doctor in doctors:
        keyboard.append([InlineKeyboardButton(doctor[1], callback_data=f'doctor_{doctor[0]}')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Выберите врача:", reply_markup=reply_markup)
    return CHOOSING_DOCTOR


async def doctor_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает выбор врача пользователем, сохраняет ID выбранного врача в контексте, извлекает данные выбранного
     врача, выводит сообщение с именем врача и предлагает выбрать услугу, формируя соответствующую клавиатуру, переходя
     в состояние CHOOSING_SERVICE, или сообщает об ошибке, если врач не найден, завершая диалог."""
    query = update.callback_query
    await query.answer()
    doctor_id = int(query.data.split('_')[1])
    context.user_data['doctor_id'] = doctor_id
    doctor = database.get_doctor_by_id(doctor_id)
    if doctor:
        doctor_name = doctor['name']
        await query.edit_message_text(text=f"Вы выбрали врача: {doctor_name}. Выберите услугу.")
        services = database.get_services()
        keyboard = [[InlineKeyboardButton(service[1], callback_data=f'service_{service[0]}')] for service in services]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Выберите услугу:",
                                       reply_markup=reply_markup)
        return CHOOSING_SERVICE
    else:
        await query.edit_message_text(text="Ошибка: Врач не найден.")
        return ConversationHandler.END

async def service_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает выбор услуги пользователем, сохраняет ID выбранной услуги в контексте, извлекает имя выбранной
    услуги, выводит сообщение с именем услуги и переходит к выбору даты и времени, вызывая choose_datetime, или сообщает
    об ошибке, если услуга не найдена, завершая диалог."""
    query = update.callback_query
    await query.answer()
    service_id = int(query.data.split('_')[1])
    context.user_data['service_id'] = service_id
    service_name = database.get_service_name(service_id)
    if service_name:
        await query.edit_message_text(text=f"Вы выбрали услугу: {service_name}. Выберите дату и время.")
        return await choose_datetime(update, context)
    else:
        await query.edit_message_text(text=f"Ошибка: Услуга с ID {service_id} не найдена.")
        return ConversationHandler.END


async def choose_datetime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Извлекает список доступных дат из базы данных, формирует Inline-клавиатуру с кнопками, каждая из которых
    представляет дату, и отправляет сообщение пользователю с просьбой выбрать дату, устанавливая состояние диалога
    CHOOSING_DATE_TIME."""
    dates = database.get_dates()
    keyboard = [[InlineKeyboardButton(str(date), callback_data=f'date_{date}')] for date in dates]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Выберите дату:", reply_markup=reply_markup)
    return CHOOSING_DATE_TIME

async def date_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает выбор даты пользователем, сохраняет выбранную дату в контексте, извлекает список доступного времени
    из базы данных, формирует Inline-клавиатуру с кнопками, представляющими время, и обновляет сообщение с просьбой
    выбрать время, сохраняя состояние диалога CHOOSING_DATE_TIME."""
    query = update.callback_query
    context.user_data['date'] = query.data.split('_')[1]
    await query.answer()
    times = database.get_times()
    keyboard = [[InlineKeyboardButton(str(time), callback_data=f'time_{time}')] for time in times]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Выберите время:", reply_markup=reply_markup)
    return CHOOSING_DATE_TIME

async def time_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает выбор времени пользователем, сохраняет его в контексте, выводит сообщение с выбранными датой и
    временем и завершает диалог."""
    query = update.callback_query
    context.user_data['time'] = query.data.split('_')[1]
    await query.answer()
    await query.edit_message_text(text=f"Вы выбрали дату: {context.user_data['date']}\nВремя: {context.user_data['time']}")
    return ConversationHandler.END

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(choose_doctor, pattern='^appointment$')],
        states={
            CHOOSING_DOCTOR: [CallbackQueryHandler(doctor_selected, pattern='^doctor_')],
            CHOOSING_SERVICE: [CallbackQueryHandler(service_selected, pattern='^service_')],
            CHOOSING_DATE_TIME: [CallbackQueryHandler(date_selected, pattern='^date_'),
                                 CallbackQueryHandler(time_selected, pattern='^time_')],
        },
        fallbacks=[],
    )
    application.add_handler(conv_handler)

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    button_handler = CallbackQueryHandler(button_handler)
    application.add_handler(button_handler)

    application.run_polling()
