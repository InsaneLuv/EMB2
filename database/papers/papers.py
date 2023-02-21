import re
import sqlite3 as sq

base = sq.connect('manager.db')
cur = base.cursor()
async def reg_papers(userid,content,date):
    cur.execute(
        'INSERT INTO papers VALUES (?,?,?)',
        (userid, content, date)
    )
    base.commit()
