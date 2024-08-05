import sqlite3
con = sqlite3.connect("mafiadb.db")
cur = con.cursor()
sql = """\
CREATE TABLE IF NOT EXISTS mafia (
    id_user INTEGER PRIMARY KEY,
    username TEXT,
    generated TEXT,
    answered TEXT
);

CREATE TABLE IF NOT EXISTS perm_ids (
    id_user INTEGER PRIMARY KEY,
    username TEXT
);

ALTER TABLE mafia
DELETE COLUMN temp_one

ALTER TABLE mafia
ADD COLUMN temp TEXT 

ALTER TABLE perm_ids
ADD COLUMN complete INTEGER DEFAULT 0
"""
try:
    cur.executescript(sql)
except sqlite3.DatabaseError as err:
    print("Ошибка: ", err)
else:
    print("Успешно.")
cur.close()
con.close()