import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3

db = SQLAlchemy()
migrate = Migrate()

# Configure SQLite pragma (WAL or DELETE mode)
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        disable_wal = os.getenv('SQLITE_DISABLE_WAL', 'false').lower() == 'true'
        
        if disable_wal:
            cursor.execute("PRAGMA journal_mode=DELETE")
        else:
            try:
                cursor.execute("PRAGMA journal_mode=WAL")
                cursor.execute("PRAGMA synchronous=NORMAL")
            except sqlite3.OperationalError:
                # Fallback to DELETE mode if WAL is unsupported (e.g. in Docker on Windows mounts)
                cursor.execute("PRAGMA journal_mode=DELETE")
                
        cursor.close()
