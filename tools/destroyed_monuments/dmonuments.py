async def get_destroyed_monuments():
    with open("destroyedmonuments.txt", 'r', encoding="utf-8") as f:
        return [line.rstrip('\n') for line in f]

