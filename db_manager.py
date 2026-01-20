import sqlite3
import os

# 1. Absolute path to your database
DB_PATH = "/Users/aidanshotland/Desktop/newsletter/articles.db"

def rebuild():
    # Delete the old file if it exists to clear the "no such table" errors
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("🗑️ Old database file removed.")

    # 2. Create the table from scratch with the correct 2026 structure
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        link TEXT UNIQUE,
        source TEXT,
        title TEXT,
        summary TEXT,
        is_read INTEGER DEFAULT 0,  -- 0 = Unread, 1 = Read
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()
    print(f"✅ Success! Created a fresh table 'articles' with 'is_read' column at: {DB_PATH}")

if __name__ == "__main__":
    rebuild()