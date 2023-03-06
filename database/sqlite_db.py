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
    
    
    base.execute('CREATE TABLE IF NOT EXISTS events_new'
                 '('
                 'uuid TEXT,'
                 'creator_tg_id INT,'
                 'event_title TEXT,'
                 'event_description TEXT,'
                 'event_message_url TEXT,'
                 'type TEXT'
                 ')'
                 )
    
    base.execute('CREATE TABLE IF NOT EXISTS profile_settings_cooldown'
                 '('
                 'tg_id INT,'
                 'bounty_cd TEXT,'
                 'game_name_cd TEXT,'
                 'clan_cd TEXT'
                 ')'
                 )

    base.execute(f'CREATE TABLE IF NOT EXISTS weeks'
        '('
        'uuid TEXT,'
        'date TEXT,'
        'special_building TEXT'
        ')'
        )

    base.execute(f'CREATE TABLE IF NOT EXISTS settings'
        '('
        'uuid TEXT,'
        's_police INT,'
        's_police_heli INT,'
        's_police_car INT,'
        's_ordinary INT,'
        's_dragon INT,'
        's_pdragon INT,'
        's_alien INT,'
        's_rat INT,'
        's_monument INT'
        ')'
        )
    
    base.execute(f'CREATE TABLE IF NOT EXISTS access'
        '('
        'uuid TEXT,'
        'tg_id INT PRIMARY KEY,'
        'game_name TEXT'
        ')'
        )
    
    base.execute(f'CREATE TABLE IF NOT EXISTS rabbit_event_members'
        '('
        'tg_id INT PRIMARY KEY,'
        'game_name TEXT,'
        'points INT'
        ')'
        )

    base.commit()