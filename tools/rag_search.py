import sqlite3
import argparse
from google.cloud import bigquery

def search_sqlite(query, db_path='C:/Yuki_Local/database/yuki_knowledge.db'):
    print(f"--- Searching SQLite: {db_path} ---")
    results = []
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Generic broad search over characters table
        sql = f"SELECT name_romaji, description FROM characters WHERE description LIKE '%{query}%' OR name_romaji LIKE '%{query}%' LIMIT 5"
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            results.append(f"[SQLite] Found: {row[0]}")
            print(f"   found: {row[0]}")
        conn.close()
    except Exception as e:
        print(f"   ❌ SQLite error: {e}")
    return results

def search_bigquery(query):
    print(f"--- Searching BigQuery Knowledge Base ---")
    results = []
    try:
        client = bigquery.Client()
        # Sanitize query for SQL 
        safe_query = query.replace("'", "\\'")
        sql = f"SELECT title, content FROM `yuki_memory.knowledge_base` WHERE content LIKE '%{safe_query}%' LIMIT 5"
        query_job = client.query(sql)
        for row in query_job.result():
            results.append(f"[BigQuery] {row.title}")
            print(f"   found: {row.title}")
    except Exception as e:
        print(f"   ❌ BigQuery error: {e}")
    return results

def main():
    parser = argparse.ArgumentParser(description="Search local SQLite and Cloud BigQuery knowledge bases.")
    parser.add_argument("query", help="Search query string")
    args = parser.parse_args()

    search_sqlite(args.query)
    search_bigquery(args.query)

if __name__ == "__main__":
    main()
