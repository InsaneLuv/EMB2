import sqlite3 as sq

base = sq.connect('manager.db')
cur = base.cursor()


async def profile_reg(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO profiles VALUES (?,?,?,?,?)', tuple(data.values()))
        base.commit()


async def update_adress(adress, tg_id):
    cur.execute('UPDATE profiles SET adress = ? WHERE tg_id = ?',(adress, tg_id))
    base.commit()


async def search_profile(mode,data):
    if mode == "tg_id":
        try:
            cur.execute(f"SELECT * FROM profiles WHERE tg_id = {str(data)}")
            profile = cur.fetchone()
            profile = {
            'tg_id': profile[0],
            'game_name': profile[1],
            'role': profile[2],
            'adress': profile[3],
            'unique': profile[4]
            }
            return profile
        except Exception as e:
            return None
    elif mode == "game_name":
        try:
            cur.execute(f"SELECT * FROM profiles WHERE game_name = '{str(data)}'")
            profile = cur.fetchone()
            profile = {
            'tg_id': profile[0],
            'game_name': profile[1],
            'role': profile[2],
            'adress': profile[3],
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
