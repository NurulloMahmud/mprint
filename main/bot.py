import asyncio
from aiogram import Bot, Dispatcher

API_TOKEN = '7115797697:AAFuLtVRn2-PXFBu4t8tnYiHF5BTLLAD1Is'

async def send_messages(bot_instance, users_info):
    for user_info in users_info:
        user_id = user_info['user_id']
        try:
            await bot_instance.send_message(user_id,
                f"Your order has been received:\n"
                f"Order Name: {user_info['order_name']}\n"
                f"Date: {user_info['date']}\n"
                f"Initial Payment: {user_info['initial_payment']}\n"
                f"Final Price: {user_info['final_price']}\n"
                f"Price per Product: {user_info['price_per_product']}\n"
                f"Product Quantity: {user_info['product_qty']}\n"
                f"Customer Telegram ID: {user_id}" # bu kerakmas
            )
        except Exception as e:
            print(f"Fail {user_id}: {e}")
            # print emas shu funksiya biryoli customerga jonatadigan bolsin shu datani

async def main():
    bot_instance = Bot(token=API_TOKEN)
    dp = Dispatcher()

    users_info = [
        {
            'user_id': 5431321356,
            'order_name': 'A4',
            'date': '2024-05-22',
            'initial_payment': '$260',
            'final_price': '$300',
            'price_per_product': '$26',
            'product_qty': 10,
        },
        {
            'user_id': 1547040457,
            'order_name': 'A3',
            'date': '2024-05-23',
            'initial_payment': '$200',
            'final_price': '$700',
            'price_per_product': '$70',
            'product_qty': 10,
        },
        {
            'user_id': 5431321356,
            'order_name': 'A5',
            'date': '2024-05-22',
            'initial_payment': '$260',
            'final_price': '$300',
            'price_per_product': '$26',
            'product_qty': 10,
        }
    ]

    await send_messages(bot_instance, users_info)

    await dp.start_polling(bot_instance)

if __name__ == '__main__':
    asyncio.run(main())
