import logging
import operator
import re
import sqlite3 as sq

from database.profile.profile import search_profile

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

async def event_reg2(state):
    public = {}
    private = {}
    async with state.proxy() as data:

        public['uuid'] = str(data['uuid'])
        public['creator_tg_id'] = data['creator_id']
        public['event_title'] = data['title']
        public['event_description'] = data['description']
        public['event_message_url'] = data['message_link']
        public['type'] = data['type']
        cur.execute('INSERT INTO events_new VALUES (?,?,?,?,?,?)', tuple(public.values()))

        if public['type'] == 'clan_event':
            private['uuid'] = data['uuid']
            private['weeks'] = data['weeks']
            private['rules'] = data['rules']

            for week in private['weeks']:
                date = week['date']
                building = week['special_building']
                cur.execute('INSERT INTO weeks VALUES (?,?,?)', (public['uuid'], date, building))



            raw_dict = {}
            for rule in data['rules']:
                raw_dict[rule['type']] = rule['count']

            cur.execute('INSERT INTO settings VALUES (?,?,?,?,?,?,?,?,?,?)', (
                str(private['uuid']),
                raw_dict.get('s_police', 0),
                raw_dict.get('s_police_heli', 0),
                raw_dict.get('s_police_car', 0),
                raw_dict.get('s_ordinary', 0),
                raw_dict.get('s_dragon', 0),
                raw_dict.get('s_pdragon', 0),
                raw_dict.get('s_alien', 0),
                raw_dict.get('s_rat', 0),
                raw_dict.get('s_monument', 0)
                ))
        base.commit()

async def get_eventlist():
    event_list = []
    for ret in cur.execute(f'SELECT * FROM events_new').fetchall():
        event = {'uuid': ret[0], 'creator_tg_id': ret[1], 'event_title': ret[2], 'event_description': ret[3], 'event_message_url': ret[4], 'type': ret[5]}
        event_list.append(event)
    if len(event_list) <= 0:
        event_list = None
    return event_list

async def get_by_uuid(uuid):
    result = {}
    cur.execute('''
        SELECT 
            events_new.uuid,
            events_new.creator_tg_id,
            events_new.event_title,
            events_new.event_description,
            events_new.event_message_url,
            events_new.type,
            GROUP_CONCAT(weeks.date || ',' || weeks.special_building) AS weeks,
            settings.s_police,
            settings.s_police_heli,
            settings.s_police_car,
            settings.s_ordinary,
            settings.s_dragon,
            settings.s_pdragon,
            settings.s_alien,
            settings.s_rat,
            settings.s_monument,
            GROUP_CONCAT(DISTINCT access.tg_id || ',' || access.game_name) AS access
        FROM 
            events_new
            LEFT JOIN weeks ON events_new.uuid = weeks.uuid
            LEFT JOIN settings ON events_new.uuid = settings.uuid
            LEFT JOIN access ON events_new.uuid = access.uuid
        WHERE 
            events_new.uuid = ?
        GROUP BY 
            events_new.uuid
    ''', (uuid,))



    for row in cur.fetchall():
        event_dict = {
            "uuid": row[0],
            "creator_tg_id": row[1],
            "event_title": row[2],
            "event_description": row[3],
            "event_message_url": row[4],
            "type": row[5]
        }
        if event_dict['type'] == 'clan_event':
            substrings = row[6].split(',')
            weeks = []
            for i in range(0, len(substrings), 2):
                d = {"date": substrings[i], "special_building": substrings[i+1]}
                weeks.append(d)

            settings = [
                {"type": "s_police", "count": row[7]},
                {"type": "s_police_heli", "count": row[8]},
                {"type": "s_police_car", "count": row[9]},
                {"type": "s_ordinary", "count": row[10]},
                {"type": "s_dragon", "count": row[11]},
                {"type": "s_pdragon", "count": row[12]},
                {"type": "s_alien", "count": row[13]},
                {"type": "s_rat", "count": row[14]},
                {"type": "s_monument", "count": row[15]}
            ]

            try:
                substrings2 = row[16].split(',')
                access = []
                for i in range(0, len(substrings2), 2):
                    d = {"tg_id": substrings2[i], "game_name": substrings2[i+1]}
                    access.append(d)
                access.sort(key=operator.itemgetter('game_name'))
            except:
                access = None
            
            result = {**event_dict, "weeks": weeks, "rules": settings, "access": access}
        else:
            result = {**event_dict, "access": None}
    return result

async def append_to_access(uuid, access):
    try:
        try:
            access = access.split(',')
        except:
            pass
        if type(access) == list:
            write_data = []
            for i in access:
                profile = await search_profile('tg_id', i)
                if profile != None:
                    cur.execute('INSERT INTO access VALUES (?,?,?)', (uuid,i,profile[1]))
                else:
                    cur.execute('INSERT INTO access VALUES (?,?,?)', (uuid,i,'No profile found'))
        else:
            profile = await search_profile('tg_id', access)
            if profile != None:
                cur.execute('INSERT INTO access VALUES (?,?,?)', (uuid,access,profile[1]))
            else:
                cur.execute('INSERT INTO access VALUES (?,?,?)', (uuid,access,'No profile found'))
        base.commit()
    except:
        pass

async def deny_access_by_tg_id(tg_id):
    try:
        cur.execute('DELETE FROM access WHERE tg_id =?', (tg_id,))
        base.commit()
    except:
        pass

async def reg_paper(paper_result):
    cur.execute(f"SELECT * FROM papers_archive WHERE unique_paper_id = (?)", (paper_result['unique_paper_id'],))
    paper = cur.fetchone()
    if paper == None:
        cur.execute('INSERT INTO papers_archive VALUES (?,?,?,?,?,?,?,?,?,?)',
                    (paper_result['event_uuid'],
                    paper_result['tg_id'],
                    paper_result['username'],
                    paper_result['unique_player_id'],
                    paper_result['unique_paper_id'],
                    paper_result['userpic'],
                    paper_result['username'],
                    paper_result['date'],
                    paper_result['points'],
                    False,))
        base.commit()
        return True
    else:
        return False

async def reg_player_rabbit(tg_id):
    profile = await search_profile('tg_id',tg_id)
    try:
        cur.execute('INSERT INTO rabbit_event_members VALUES (?,?,?)', (tg_id,profile['game_name'],0))
        base.commit()
        return True
    except:
        base.commit()
        return False
    
async def get_rabbit_event_member_count():
    cur.execute("SELECT COUNT(*) FROM rabbit_event_members")
    result = cur.fetchone()[0]
    return result