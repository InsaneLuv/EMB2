import random


def emoji():
    emojis = ['๐ฅถ', '๐ฅต', '๐คฌ', '๐ฑ', '๐ต', '๐', '๐ผ', '๐ป', '๐ฝ',
              '๐ซฅ', '๐ง', '๐คจ', '๐คช', '๐ธ', '๐งข', '๐ง', '๐๐ป', '๐ซต๐ป']
    random_emoji = random.choice(emojis)
    return str(random_emoji)