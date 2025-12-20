import sqlite3
from google.cloud import bigquery

def search_weird_characters():
    print("--- Searching SQLite Bank ---")
    try:
        conn = sqlite3.connect('C:/Yuki_Local/database/yuki_knowledge.db')
        cursor = conn.cursor()
        query = """
        SELECT name_romaji, description 
        FROM characters 
        WHERE description LIKE '%mysterious%' 
           OR description LIKE '%unhinged%' 
           OR description LIKE '%creepy%' 
           OR description LIKE '%power%'
        LIMIT 5
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print(f"Found: {row[0]}")
        conn.close()
    except Exception as e:
        print(f"SQLite error: {e}")

    print("\n--- Searching BigQuery Knowledge Base ---")
    try:
        client = bigquery.Client()
        query = "SELECT title, content FROM `yuki_memory.knowledge_base` WHERE content LIKE '%weird%' OR content LIKE '%unique%' LIMIT 5"
        results = client.query(query).result()
        for row in results:
            print(f"Found Knowledge: {row.title}")
    except Exception as e:
        print(f"BigQuery error: {e}")

if __name__ == "__main__":
    search_weird_characters()
