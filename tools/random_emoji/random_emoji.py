import random


def emoji():
    emojis = ['🥶', '🥵', '🤬', '😱', '😵', '😈', '🍼', '👻', '👽',
              '🫥', '🧐', '🤨', '🤪', '🕸', '🧢', '🧟', '🖕🏻', '🫵🏻']
    random_emoji = random.choice(emojis)
    return str(random_emoji)