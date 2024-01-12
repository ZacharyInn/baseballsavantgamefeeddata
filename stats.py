import sqlite3
import os

def count_total_records(database_path):
    # Connect to the SQLite database
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    try:
        # Execute a SQL query to count the total number of records in all tables
        query = "SELECT COUNT(*) FROM sqlite_master WHERE type='table';"
        cursor.execute(query)

        # Fetch the result of the query
        total_tables = cursor.fetchone()[0]

        # Iterate through all tables and sum up the record counts
        total_records = 0
        for table_name in connection.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall():
            table_name = table_name[0]
            query = f"SELECT COUNT(*) FROM {table_name};"
            cursor.execute(query)
            total_records += cursor.fetchone()[0]

        return total_records

    except sqlite3.Error as e:
        print(f"Error counting total records: {e}")

    finally:
        # Close the database connection
        connection.close()


def get_database_size(database_path):
    try:
        # Get the size of the database file
        size_bytes = os.path.getsize(database_path)

        # Convert bytes to kilobytes
        size_kb = size_bytes / 1024

        return size_kb

    except FileNotFoundError:
        print("Database file not found.")
    except Exception as e:
        print(f"Error getting database size: {e}")



def printStats(pk, dbpath, dur):
    print("Data ingested from this API Endpoint: https://baseballsavant.mlb.com/gf?game_pk=" + str(pk))
    print("Data inserted into database: " + dbpath)
    print("Total records inserted: " + str(count_total_records(dbpath)))
    time = "%.3f" % round(dur, 3)
    print("Data ingestion time: " + time + " seconds")
    print("Database size: " + str(get_database_size(dbpath)) + " KB")