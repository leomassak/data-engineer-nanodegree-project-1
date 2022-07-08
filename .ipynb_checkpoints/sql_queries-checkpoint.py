# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS fact_songplay"
user_table_drop = "DROP TABLE IF EXISTS dim_user"
song_table_drop = "DROP TABLE IF EXISTS dim_song"
artist_table_drop = "DROP TABLE IF EXISTS dim_artist"
time_table_drop = "DROP TABLE IF EXISTS dim_time"

# CREATE TABLES

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS fact_songplay (
                                songplay_id SERIAL PRIMARY KEY, 
                                start_time timestamp NOT NULL, 
                                user_id integer NOT NULL, 
                                level varchar, 
                                song_id varchar, 
                                artist_id varchar, 
                                session_id varchar, 
                                location varchar, 
                                user_agent varchar
                            );""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS dim_user (
                            user_id integer PRIMARY KEY, 
                            first_name varchar, 
                            last_name varchar, 
                            gender varchar, 
                            level varchar
                        );""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS dim_song (
                            song_id varchar PRIMARY KEY, 
                            title varchar NOT NULL, 
                            artist_id varchar, 
                            year integer, 
                            duration numeric NOT NULL
                        );""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS  dim_artist (
                            artist_id varchar PRIMARY KEY, 
                            name varchar NOT NULL, 
                            location varchar, 
                            latitude double precision, 
                            longitude double precision
                        );""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS dim_time (
                            time_id SERIAL PRIMARY KEY,
                            start_time timestamp, 
                            hour integer, 
                            day integer, 
                            week integer, 
                            month integer, 
                            year varchar, 
                            weekday varchar
                        );""")

# INSERT RECORDS

songplay_table_insert = ("""INSERT INTO fact_songplay (
                                start_time, 
                                user_id, 
                                level, 
                                song_id, 
                                artist_id, 
                                session_id, 
                                location, 
                                user_agent) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT DO NOTHING;""")

user_table_insert = ("""INSERT INTO dim_user (
                            user_id, 
                            first_name, 
                            last_name, 
                            gender, 
                            level)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (user_id) DO UPDATE SET level=EXCLUDED.level;""")

song_table_insert = ("""INSERT INTO dim_song (
                            song_id, 
                            title, 
                            artist_id, 
                            year, 
                            duration) 
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING;""")

artist_table_insert = ("""INSERT INTO dim_artist (
                            artist_id, 
                            name, 
                            location, 
                            latitude, 
                            longitude) 
                          VALUES (%s, %s, %s, %s, %s)
                          ON CONFLICT (artist_id) DO UPDATE SET
                            name = EXCLUDED.name,
                            location = EXCLUDED.location,
                            latitude = EXCLUDED.latitude,
                            longitude = EXCLUDED.longitude;""")


time_table_insert = ("""INSERT INTO dim_time (
                            start_time, 
                            hour, 
                            day, 
                            week, 
                            month, 
                            year, 
                            weekday) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING;""")

# FIND SONGS

song_select = ("""
            SELECT dim_song.song_id, dim_song.artist_id 
            FROM dim_song
            JOIN dim_artist ON dim_song.artist_id = dim_artist.artist_id
            WHERE dim_song.title = %s 
                AND dim_artist.name = %s 
                AND dim_song.duration = %s;
            """)

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]