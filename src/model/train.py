from models import SimilarityRecommender, RegressionRecommender, FactorizationRecommender


import sys
sys.path.append('src/utils')
from data_utils import load_rating_matrix

print ('Loading data from database.')
X = load_rating_matrix('data/db/movie.sqlite', item_table='movie')
model = FactorizationRecommender()
print ('Training model on data.')
model.fit(X)
model.save('models/factorization.pkl')
