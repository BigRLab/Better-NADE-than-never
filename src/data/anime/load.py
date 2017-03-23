from __future__ import print_function
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from tqdm import tqdm
import sqlite3
import csv
import io



create_anime = '''create table "anime"(
    "anime_id" integer primary key,
    "name" text,
    "genre" text,
    "type" text,
    "episodes" text,
    "rating" real,
    "members" integer);'''

create_rating = '''create table "rating"( 
    "user_id" integer, 
    "anime_id" integer, 
    "rating" integer);'''

insert_anime = 'insert into "anime" values(?,?,?,?,?,?,?);'
insert_rating = 'insert into "rating" values(?,?,?);'
remove_duplicate = 'delete from rating where rowid not in (select min(rowid) from rating group by user_id, anime_id);'

if __name__ == '__main__':
    with sqlite3.connect('data/db/anime.sqlite') as connection:
        connection.execute(create_anime)

        with io.open('data/raw/anime/anime.csv', 'r', encoding='utf-8') as handler:
            csv_reader = csv.reader(handler)
            next(csv_reader) # Skip Header

            reader = ( [int(anime_id),unicode(name),unicode(genre),unicode(anime_type),unicode(episodes),float(rating or '0'),int(members) ] 
                for anime_id,name,genre,anime_type,episodes,rating,members in tqdm(csv_reader,total=12293) )
            
            connection.executemany(insert_anime, reader)
        
        connection.execute(create_rating)
        with io.open('data/raw/anime/rating.csv', 'r', encoding='utf-8') as handler:
            csv_reader = csv.reader(handler)
            next(csv_reader) # Skip Header

            reader = ( [int(user_id),int(anime_id),int(rating) ] 
                for user_id,anime_id,rating in tqdm(csv_reader,total=7813737) )
            
            connection.executemany(insert_rating, reader)
        
        # Remove duplicate ratings
        connection.execute(remove_duplicate)