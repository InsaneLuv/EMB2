# @dp.message_handler(Command("menu"))
# async def menu(message: types.Message):
#     if lambda: message.from_user.id in admins:
#         await message.reply("💼 Админ-мод", reply_markup=admin_kb_menu)
#     else:
#         await message.reply("💼 Юзер-мод", reply_markup=user_kb_menu)