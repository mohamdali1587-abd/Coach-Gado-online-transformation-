import sqlite3
from pathlib import Path
DB=Path("data/media_engine.db")
DB.parent.mkdir(parents=True,exist_ok=True)
def connect():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
def init():
    with connect() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS jobs(
        id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        topic TEXT, script TEXT, caption TEXT, video_path TEXT, status TEXT,
        publish_id TEXT, error TEXT
        )""")
def add(topic,script,caption,video_path,status,publish_id="",error=""):
    with connect() as c:
        cur=c.execute("INSERT INTO jobs(topic,script,caption,video_path,status,publish_id,error) VALUES(?,?,?,?,?,?,?)",
        (topic,script,caption,video_path,status,publish_id,error)); return cur.lastrowid
def recent(limit=30):
    with connect() as c: return [dict(r) for r in c.execute("SELECT * FROM jobs ORDER BY id DESC LIMIT ?",(limit,))]
