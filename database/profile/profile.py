import logging
import sqlite3 as sq

base = sq.connect('manager.db')
cur = base.cursor()


async def profile_reg(state):
    cur.execute('INSERT INTO profiles VALUES (?,?,?,?,?)', (state["tg_id"], state["game_name"], state["role"], state["address"], state["unique"], ))
    base.commit()


async def update_address(address, tg_id):
    cur.execute('UPDATE profiles SET address = ? WHERE tg_id = ?',(address, tg_id))
    base.commit()


async def search_profile(mode,data):
    try:
        cur.execute(f"SELECT * FROM profiles WHERE {mode} = (?)", (data,))
        profile = cur.fetchone()
        profile = {
        'tg_id': profile[0],
        'game_name': profile[1],
        'role': profile[2],
        'address': profile[3],
        'unique': profile[4]
        }
        return profile
    except Exception as e:
        return None

async def lang_reg(id,lang):
    try:
        cur.execute('INSERT INTO lang VALUES (?,?)', (id,lang))
        base.commit()
    except Exception as e:
        cur.execute('UPDATE lang SET lang=? where tg_id=?', (lang,id))
        base.commit()

async def search_lang(id):
    try:
        cur.execute(f"SELECT * FROM lang WHERE tg_id = {str(id)}")
        profile = cur.fetchone()
        return profile[1]
    except:
        await lang_reg(id,'en')
        return 'en'

async def get_profile_settings_cd(tg_id):
    cur.execute(f"SELECT * FROM profile_settings_cooldown WHERE tg_id = {int(tg_id)}")
    cooldown = cur.fetchone()
    if cooldown != None:
        cooldown = {
        'bounty_cd': cooldown[1],
        'game_name_cd': cooldown[2],
        'clan_cd': cooldown[3]
        }
    else:
        cooldown = {
        'bounty_cd': '2000-01-01',
        'game_name_cd': '2000-01-01',
        'clan_cd': '2000-01-01'
        }
        cur.execute('INSERT INTO profile_settings_cooldown VALUES (?,?,?,?)', (tg_id,cooldown["bounty_cd"],cooldown["game_name_cd"],cooldown["clan_cd"]))
        base.commit()
    return cooldown

async def set_profile_settings_cd(setting, tg_id, date):
    cur.execute(f'UPDATE profile_settings_cooldown SET {setting}=? where tg_id=?', (date,tg_id))
    base.commit()