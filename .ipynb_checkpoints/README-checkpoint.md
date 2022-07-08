# Sparkify 
This a project to apply data modeling with PostgreSQL and build an ETL
pipeline using Python to process the required data and insert into tables, designing a star schema.

The star schema will provide a faster data access and derive businness insights in a simpler way.

## Project Description
A startup called Sparkify wants to analyze the data
they've been collecting on songs and user activity on their new music streaming
app. The analytics team is particularly interested in understanding what songs
users are listening to. Currently, they don't have an easy way to query their
data, which resides in a directory of JSON logs on user activity on the app, as
well as a directory with JSON metadata on the songs in their app.

They'd like a data engineer to create a Postgres database with tables designed to optimize queries on song play analysis, and bring you on the project.

### Datasets
We will use two datasets: _Songs_ and _Logs_

#### Songs dataset
The Song data contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID.

Below an exemple of the Song data payload:

```javascript
{
    "num_songs": 1,
    "artist_id": "AR7G5I41187FB4CE6C",
    "artist_latitude": null,
    "artist_longitude": null,
    "artist_location": "London, England",
    "artist_name": "Adam Ant",
    "song_id": "SONHOTT12A8C13493C",
    "title": "Something Girls",
    "duration": 233.40363,
    "year": 1982
}

```
#### Logs dataset
The Log data contains files in JSON format generated by a event simulator based on the songs in the dataset above. These simulate activity logs from a music streaming app based on specified configurations.

Below an exemple of the Log data payload:

```javascript
{
    "artist": null,
    "auth": "Logged In",
    "firstName": "Walter",
    "gender": "M",
    "itemInSession": 0,
    "lastName": "Frye",
    "length": null,
    "level": "free",
    "location": "San Francisco-Oakland-Hayward, CA",
    "method": "GET",
    "page": "Home",
    "registration": 1540919166796.0,
    "sessionId": 38,
    "song": null,
    "status": 200,
    "ts": 1541105830796,
    "userAgent": "\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36\"",
    "userId": "39"
}
```

### Process
#### Database
The script: `create_tables.py` will import all the queries stored in `sql_queries` and will execute them ir order to built the project database.

If there's any changes in the tables structure, running the script again will drop and recriate all tables with the changes applied.

#### ETL
The script `etl.py` provides all the functions to perform the ETL process.

#### Tests
The scrip `test.ipynb` provides multiple test cases indicating the best types and statements for queries in the project

## Project Instructions
### Create database and tables
- For the first execution, run `python create_tables.py` to create the database and tables.
- To rebuild de database, close all psycopg2 connections and run `python create_tables.py` again to drop and recriate all tables

### ETL Process
- After creating the database and tables, run `python etl.py`  to execute all the data process, data transformations and table inserts.