import sqlite3
con = sqlite3.connect("mafiadb.db")
cur = con.cursor()
sql = """\
CREATE TABLE mafia (
    id_user INTEGER PRIMARY KEY
    
"""
con.close()