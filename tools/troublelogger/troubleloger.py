from datetime import datetime


async def troublelog(user,log,answer):
    try:
        now = datetime.now()
        trouble = f'┌——————————————————————————————————————┐\n\n' \
                  f'{now.strftime("%d-%m-%Y %H:%M")}\n' \
                  f'@{user} trouble:\n\n' \
                  f'{log}\n\n' \
                  f'message text:\n\n' \
                  f'{answer}\n\n' \
                  f'└——————————————————————————————————————┘\n\n'
        with open("troublelogs/tlogs.txt", 'a', encoding="utf-8") as f:
            f.write(trouble)
    except:
        pass

