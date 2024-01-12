import sqlite3
import requests
import json
import os
import time
import tables
import stats


#main function
def main():
    #get game PK from user
    game_pk = input("Enter game PK: ")
    
    #create API URL
    api_url = 'https://baseballsavant.mlb.com/gf?game_pk=' + str(game_pk)

    #get game feed data
    response = requests.get(api_url)
    game_feed_data = response.json()
    #for invalid game PKs
    if 'error' in game_feed_data.keys():
        print(f"Invalid Game PK")
        print(f"Exiting program.")
        exit()
    #if data fetching is successful
    elif response.status_code == 200:
        print("Data fetched successfully.")
    #if data fetching is unsuccessful (not invalid game PK)
    else:
        print(f"Error fetching data. Status code: {response.status_code}")
        print(f"Exiting program.")
        exit()

    #create database
    dbYN = input("Do you want to create your database in a specific filepath?\nIf you select 'N', the database will be created in the local directory (Y/N): ")
    if dbYN == 'Y':
        db_directory = input("Enter filepath: ")
        df_filename = 'savantfeed.db'
        db_path = os.path.join(db_directory, df_filename)

        if not os.path.exists(db_directory):
            decision = input("Directory does not exist. Do you want to create it? (Y/N): ")
            if decision == 'Y':
                os.makedirs(db_directory)
            elif decision == 'N':
                print("Exiting program.")
                exit()
            else: 
                print("Invalid input.")
                print("Exiting program.")
                exit()

        connection = sqlite3.connect(db_path)

        cur = connection.cursor()

        #create tables
        tables.create_tables(db_path)

        #start timer
        start_time = time.time()

        #insert data into tables
        tables.insert_data(connection, game_feed_data)

        #end timer
        end_time = time.time()

        #calculate time elapsed
        duration = end_time - start_time

        #print out summary stats
        stats.printStats(game_pk, db_path, duration)

    elif dbYN == 'N':
        db_file = 'savantfeed.db'

        connection = sqlite3.connect(db_file)

        cur = connection.cursor()

        #create tables
        tables.create_tables(db_file)

        #start timer
        start_time = time.time()

        #insert data into tables
        tables.insert_data(connection, game_feed_data)

        #end timer
        end_time = time.time()

        #calculate time elapsed
        duration = end_time - start_time

        #print out summary stats
        stats.printStats(game_pk, db_file, duration)

    else:
        print("Invalid input.")
        print("Exiting program.")
        exit()

    connection.close()
    
if __name__ == "__main__":
    main()