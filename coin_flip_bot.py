import asyncio
import telebot.async_telebot as telebot
from sqlalchemy import update, select
from telebot import types
import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from database.engine import drop_db, create_db, session_maker
from database.models import User

bot = telebot.AsyncTeleBot(token=os.getenv("BOT_TOKEN"))
ADMIN_1 = os.getenv("ADMIN_USERNAME_1")
ADMIN_2 = os.getenv("ADMIN_USERNAME_2")
TARGET_CHANNEL = os.getenv("TARGET_CHANNEL")


async def is_subscriber(channel_id, user_id):
    try:
        subscription = await bot.get_chat_member(channel_id, user_id)
        if subscription.status in ['member', 'administrator', 'creator']:
            return True
        else:
            return False
    except Exception as e:
        print("Error:", e)
        return False


@bot.message_handler(commands=['start'])
async def start(message):
    async with session_maker() as session:
        user_find = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
        if user_find.scalar_one_or_none() is None:
            user = User(username=message.from_user.username, telegram_id=message.from_user.id, full_name=message.from_user.full_name, casino_id=None)
            session.add(user)
            await session.commit()
    keyboardmain = types.InlineKeyboardMarkup(row_width=1)
    subscribe_button = types.InlineKeyboardButton(text="Подписаться", url="https://t.me/+xp6CPmE9tzoyZmEy")
    check_button = types.InlineKeyboardButton(text="Проверить", callback_data="check_subscription")
    keyboardmain.add(subscribe_button, check_button)
    await bot.send_message(message.chat.id, f"Добро пожаловать, {message.from_user.full_name} \n\nДля использования бота - подпишись на наш канал!", reply_markup=keyboardmain)


@bot.callback_query_handler(func=lambda call:True)
async def callback_inline(call):
    if call.data == "check_subscription":
        # Здесь ваш код для проверки подписки пользователя на канал
        # После проверки отправляем сообщение с результатом
        if await is_subscriber(channel_id=TARGET_CHANNEL,
                         user_id=call.message.chat.id
                         ):
            call.data = "subscriber"
        else:
            await bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Вы не подписаны на канал")
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)

    if call.data == "subscriber":
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        register_button = types.InlineKeyboardButton(text="📱 Регистрация", callback_data="registration")
        instruction_button = types.InlineKeyboardButton(text="📚 Инструкция", callback_data="instruction")
        get_signal_button = types.InlineKeyboardButton(text="🪙 Подбросить монетку 🪙", callback_data="get_signal")
        keyboard.add(register_button, instruction_button, get_signal_button)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        await bot.send_message(chat_id=call.message.chat.id, text="Добро пожаловать в 🔸Brawl Bot🔸!\n\n"
                                                                  "💀Brawl Pirates - это игра в букмекерской конторе 1win, которая основывается на выборе “Черепа”.\n"
                                                                  "В этой игре пользователи смогут испытать свою удачу и найти сокровища пиратов, выиграв тем самым реальные деньги.\n\n\n"
                                                                  "Игра предлагает каждому выбрать один из трёх черепов и угадать, в каком из них находится сокровище.Наш бот основан на нейросети CLAUD-3.\n"
                                                                  "Он может предугадать результат с вероятностью 97%.",
                         reply_markup=keyboard
                         )

    if call.data == "registration":
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        register_button = types.InlineKeyboardButton(text="📱 Зарегистрироваться", url='https://1wytvn.life/?open=register#q7r9')
        back_button = types.InlineKeyboardButton(text="🔙 Вернуться в главное меню", callback_data="subscriber")
        keyboard.add(register_button, back_button)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        await bot.send_photo(chat_id=call.message.chat.id,
                             photo=open('resources/registration.JPG', 'rb'),
                         caption="🟡 1. Для начала зарегистрируйтесь по ссылке на сайте <a href='https://1wytvn.life/?open=register#q7r9' style='text-decoration:none'>1WIN (CLICK)</a>\n"
                              "🟡 2. После успешной регистрации cкопируйте ваш айди на сайте (Вкладка 'пополнение' и в правом верхнем углу будет ваш ID).)\n"
                              "🟡 3. И отправьте его боту в ответ на это сообщение!",
                         reply_markup=keyboard,
                         parse_mode='HTML'
                             )


    if call.data == "instruction":
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        back_button = types.InlineKeyboardButton(text="🔙 Вернуться в главное меню", callback_data="subscriber")
        keyboard.add(back_button)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        await bot.send_photo(chat_id=call.message.chat.id,photo=open('resources/instruction.PNG', 'rb') , caption="Бот основан и обучен на кластере нейросети 🖥 [bitsGap].\n\n"
                                                                  "Для тренировки бота было сыграно 🎰10.000+ игр.\n"
                                                                  "В данный момент пользователи бота успешно делают в день 15-25% от своего 💸 капитала!\n\n"
                                                                  "На текущий момент бот по сей день проходит проверки и  исправления! Точность бота составляет 97%!\n\n"
                                                                  "Для получения максимального профита следуйте следующей инструкции:\n\n"
                                                                  "🟡 1. Пройти регистрацию в букмекерской конторе <a href='https://1wytvn.life/?open=register#q7r9' style='text-decoration:none'>1WIN (CLICK)</a>\n"
                                                                  "Если не открывается - заходим с включенным VPN (Швеция). В Play Market/App Store полно бесплатных сервисов, например: Vpnify, Planet VPN, Hotspot VPN и так далее!\n\n"
                                                                  "Без регистрации доступ к сигналам не будет открыт!\n\n"
                                                                  "🟡 2. Пополнить баланс своего аккаунта.\n\n"
                                                                  "🟡 3. Перейти в раздел 1win games и выбрать игру  🪙'CoinFlip.\n\n"
                                                                  "🟡 4. Нажать в боте кнопку «подбросить монету» и ставить по сигналу бота.\n\n"
                                                                  "🟡 5. При неудачном сигнале советуем удвоить(Х²) ставку что бы полностью перекрыть потерю при следующем сигнале.",
                         reply_markup=keyboard,
                         parse_mode="HTML"
                             )

    if call.data == "get_signal":
        async with session_maker() as session:
            user1 = await session.execute(select(User).where(User.telegram_id == call.message.chat.id))
            user2 = await session.execute(select(User).where(User.telegram_id == call.message.chat.id))
            if (user1.scalar_one_or_none() is None) or (user2.scalar_one_or_none().casino_id is None):
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                register_button = types.InlineKeyboardButton(text="📱 Зарегистрироваться",
                                                             url='https://1wytvn.life/?open=register#q7r9')
                keyboard.add(register_button)
                await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
                await bot.send_message(chat_id=call.message.chat.id, text="Пожалуйста, зарегистрируйтесь перед получением сигнала", reply_markup=keyboard)
            else:
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                webapp = types.WebAppInfo("https://yecoinflip.ru/")
                apple_app_button = types.InlineKeyboardButton(text="🍏 Открыть Web app IOS", web_app=webapp)
                android_app_button = types.InlineKeyboardButton(text="🤖 Открыть Android | WINDOWS", web_app=webapp)
                back_button = types.InlineKeyboardButton(text="🔙 Вернуться в главное меню", callback_data="subscriber")
                keyboard.add(apple_app_button, android_app_button, back_button)
                await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
                await bot.send_message(chat_id=call.message.chat.id, text="ВЕБ Приложение:", reply_markup=keyboard)


    if call.data == "close_menu":
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)

@bot.message_handler(func=lambda message: message.text.isdigit() and len(message.text) <= 10)
async def handle_custom_number(message):
    async with session_maker() as session:
        user1 = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
        user2 = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
        if user1.scalar_one_or_none() and (user2.scalar_one_or_none().casino_id is None):
            await session.execute(update(User).where(User.telegram_id == message.from_user.id).values(casino_id=message.text))
            await session.commit()
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            instruction_button = types.InlineKeyboardButton(text="📚 Инструкция", callback_data="instruction")
            get_signal_button = types.InlineKeyboardButton(text="🪙 Подбросить монетку 🪙", callback_data="get_signal")
            close_menu_button = types.InlineKeyboardButton(text="❌ Закрыть окно", callback_data="close_menu")
            keyboard.add(get_signal_button, instruction_button, close_menu_button)
            await bot.send_message(message.chat.id, "Вы успешно зарегестрированы! Теперь у вас есть доступ к сигналам.", reply_markup=keyboard)


@bot.message_handler(func=lambda message: (message.text and not (message.text.isdigit())) and (message.from_user.username == ADMIN_1 or message.from_user.username == ADMIN_2))
async def handle_admin_post(message):
    async with session_maker() as session:
        result = await session.execute(select(User))
        users = result.scalars()
        for user in users:
            await bot.send_message(chat_id=user.telegram_id, text=message.text)


@bot.message_handler(content_types=['photo', 'document', 'video'])
async def handle_admin_post_photo(message):
    print(message)
    if (message.from_user.username == ADMIN_1) or (message.from_user.username == ADMIN_2):
        async with session_maker() as session:
            result = await session.execute(select(User))
            users = result.scalars()
            for user in users:
                await bot.copy_message(chat_id=user.telegram_id, from_chat_id=message.chat.id, message_id=message.id)


async def on_shutdown(bot):
    print('Bot shut down...')


async def on_startup(bot):
    run_param = False
    if run_param:
        await drop_db()

    await create_db()

async def main():
    await on_startup(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.polling(none_stop=True)

asyncio.run(main())