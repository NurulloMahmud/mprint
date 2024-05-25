import asyncio
from aiogram import Bot, Dispatcher

API_TOKEN = '7115797697:AAFuLtVRn2-PXFBu4t8tnYiHF5BTLLAD1Is'

async def send_messages(bot_instance, users_info):
    for user_info in users_info:
        user_id = user_info['user_id']
        try:
            await bot_instance.send_message(
                user_id,
                f"Your order has been received:\n"
                f"Order Name: {user_info['order_name']}\n"
                f"Date: {user_info['date']}\n"
                f"Initial Payment: {user_info['initial_payment']}\n"
                f"Final Price: {user_info['final_payment']}\n"
                f"Price per Product: {user_info['price_per_product']}\n"
                f"Product Quantity: {user_info['products_qty']}\n"
            )
        except Exception as e:
            print(f"Failed to send message to {user_id}: {e}")

async def main(users_info):
    try:
        bot_instance = Bot(token=API_TOKEN)
        dp = Dispatcher()

        await send_messages(bot_instance, users_info)

        await dp.start_polling(bot_instance)

        await bot_instance.close()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    asyncio.run(main(user_info))
