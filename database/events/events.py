import re
import sqlite3 as sq

base = sq.connect('manager.db')
cur = base.cursor()


async def event_reg(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO events VALUES (?,?,?,?,?,?)', tuple(data.values()))
        event_info = tuple(data.values())
        cur.execute('INSERT INTO events_point_settings VALUES (?,?)', (event_info[1],'None'))
        base.commit()


async def event_update(mode,data, old_data):
    if mode == "name":
        cur.execute('UPDATE events SET event_name=? where event_name=?', (data, old_data))
    elif mode == "description":
        cur.execute('UPDATE events SET event_description=? where event_name=?', (data, old_data))
    elif mode == "url":
        cur.execute('UPDATE events SET event_message_url=? where event_name=?', (data, old_data))
    elif mode == "state":
        cur.execute('UPDATE events SET state=? where event_name=?', (data, old_data))
    elif mode == "access":
        re_data = re.sub('\n', '', data)
        cur.execute('UPDATE events SET access=? where event_name=?', (re_data, old_data))
    elif mode == "psettings":
        re_data = re.sub('\n', ',', data)
        cur.execute('UPDATE events_point_settings SET rules=? where event_name=?', (re_data, old_data))
    base.commit()


async def event_read(state="current"):
    event_list = []
    if state == "current":
        for ret in cur.execute(f'SELECT * FROM events WHERE state = "True"').fetchall():
            event_list.append(ret)
    else:
        for ret in cur.execute(f'SELECT * FROM events').fetchall():
            event_list.append(ret)

    if event_list: return event_list
    else: return None

async def get_psettings(event_name):
    cur.execute(f"SELECT * FROM events_point_settings WHERE event_name = (?)", (event_name,))
    psettings = cur.fetchone()
    return psettings[1]

async def inline_helper(data):
    cur.execute(f"SELECT * FROM events WHERE event_name = (?)",(data,))
    event = cur.fetchone()
    return event


async def search_event(event_name):
    cur.execute(f"SELECT * FROM events WHERE event_name = (?)", (event_name,))
    event = cur.fetchone()
    return event
