from __future__ import print_function
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from tqdm import tqdm
import sqlite3
import csv
import io



create_movie = '''create table "movie"(
    "movie_id" integer primary key,
    "name" text,
    "genre" text);'''

create_rating = '''create table "rating"( 
    "user_id" integer, 
    "movie_id" integer, 
    "rating" integer);'''

insert_movie = 'insert into "movie" values(?,?,?);'
insert_rating = 'insert into "rating" values(?,?,?);'
remove_duplicate = 'delete from rating where rowid not in (select min(rowid) from rating group by user_id, movie_id);'

def custom_csv_reader(handle, delimiter=','):
    for line in handle:
        yield line.split(delimiter)

if __name__ == '__main__':
    with sqlite3.connect('data/db/movie.sqlite') as connection:
        connection.execute(create_movie)

        with io.open('data/raw/ml-1m/movies.dat', 'r', encoding='latin1') as handler:
            csv_reader = custom_csv_reader(handler, delimiter='::')

            reader = ( [int(movie_id),unicode(name),unicode(genre) ] 
                for movie_id,name,genre in tqdm(csv_reader,total=3883, desc='processing movies') )
            
            connection.executemany(insert_movie, reader)
        
        connection.execute(create_rating)
        with io.open('data/raw/ml-1m/ratings.dat', 'r', encoding='latin1') as handler:
            csv_reader = custom_csv_reader(handler, delimiter='::')

            reader = ( [int(user_id),int(movie_id),int(rating) ] 
                for user_id,movie_id,rating,_ in tqdm(csv_reader,total=1000209,desc='processing ratings') )
            
            connection.executemany(insert_rating, reader)
        
        # Remove duplicate ratings
        connection.execute(remove_duplicate)