import scipy.sparse as sparse
from pandas import read_sql
import sqlite3



def load_rating_matrix(db_path, item_table='anime'):
    item_id_column = '{0}_id'.format(item_table)
    item_index_column = '{0}_index'.format(item_table)
    rating_query = 'select user_id, {0}, rating from rating;'.format(item_id_column)
    item_query = 'select {0} from {1};'.format(item_id_column, item_table)
    user_query = 'select distinct rating.user_id from rating;'
    
    with sqlite3.connect(db_path) as connection:

        # Load data
        rating = read_sql(rating_query, connection)
        item = read_sql(item_query, connection)
        user = read_sql(user_query, connection)
    
    user['user_index'] = list(range(len(user)))
    item[item_index_column] = list(range(len(item)))

    rating = rating.merge(user, on='user_id').merge(item, on=item_id_column)

    row =  rating[item_index_column]
    col = rating.user_index
    data = rating.rating
    matrix = sparse.coo_matrix((data, (row, col))).tocsr()

    return matrix
