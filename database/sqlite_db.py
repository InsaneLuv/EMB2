import logging
import sqlite3 as sq


async def sql_start():
    global base, cur
    base = sq.connect('manager.db')
    cur = base.cursor()
    
    if base:
        logging.info("Data base connected!")

    base.execute('CREATE TABLE IF NOT EXISTS profiles('
                 'tg_id PRIMARY KEY,'
                 'game_name TEXT,'
                 'role TEXT)')

    base.execute('CREATE TABLE IF NOT EXISTS events('
                 'creator_tg_id TEXT,'
                 'event_name TEXT,'
                 'event_description TEXT,'
                 'event_message_url TEXT,'
                 'state TEXT,'
                 'access TEXT)')

    base.commit()