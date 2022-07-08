import os
import json
import glob
import psycopg2
import pandas as pd
import numpy as np

from psycopg2.extensions import register_adapter, AsIs
from sql_queries import *

register_adapter(np.int64, AsIs)
register_adapter(np.float64, AsIs)


def process_song_file(cur, filepath):
    """
    This function will read a song file, select the songs and artists columns, 
    and insert the data into songs and artists dimension tables
    Parameters:
        cur (cursor): psycopg2 cursor connection to postgreSQL
        filepat: Path to the song file that will be read
    """
    
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].fillna(0).values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']] \
                  .fillna(0) \
                  .values[0] \
                  .tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    This function will read a log file, select the time and users columns, 
    and insert the data into time and users dimension tables
    Parameters:
        cur (cursor): psycopg2 cursor connection to postgreSQL
        filepat: Path to the log file that will be read
    """
                    
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.loc[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = (t, t.dt.hour, t.dt.day, t.dt.week, t.dt.month, t.dt.year, t.dt.weekday)
    column_labels = ("start_time", "hour", "day", "week", "month", "year", "weekday")
    time_df = pd.concat(time_data, keys=column_labels, axis=1)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']].drop_duplicates()

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)
                      
    # Converts df timestamp
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Get all json files from the filepath and process each file, storing data into the database

    Parameters:
        cur: psycopg2 cursor connection to postgreSQL
        conn: psycopg2 connection object
        filepath (string): path where the json files are located
        func (function): function to execute
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    The main function executes all etl process and functions on run the script
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()