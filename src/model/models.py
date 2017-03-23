from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition.truncated_svd import TruncatedSVD
from sklearn.linear_model import LinearRegression
from numpy import zeros, concatenate
from collections import defaultdict
from lightfm import LightFM
import json
from tqdm import tqdm
from pickle import Pickler, Unpickler, HIGHEST_PROTOCOL

class SimilarityRecommender(object):
    def __init__(self, feature_size=10):
        self.feature_size = feature_size
        self.svd = TruncatedSVD(n_components=feature_size)
        self.rating = None

    def fit(self, rating):
        # rating (item x user)
        self.rating = rating
        item = self.svd.fit_transform(rating)
        similarity = defaultdict(lambda: dict())

        n_item, n_user = rating.shape
        for first in tqdm(range(n_item)):
            for second in range(first):
                first_item = item[first].reshape(1, -1)
                second_item = item[second].reshape(1, -1)
                similarity[first][second] = float(cosine_similarity(first_item, second_item)[0, 0])

        self.similarity = dict(similarity)
        return self

    def predict(self, user, item):
        history = self.rating[:, user].nonzero()
        absolute_score = sum(self.get_similarity(item, user_item) * rating for user_item, rating in history)
        score = float(absolute_score) / sum(rating for item, rating in history)
        return score

    def similar_to(self, item, n=5):

        return

    def get_similarity(self, item, target):
        return self.similarity[item][target] if item > target else self.similarity[target][item]

    def save(self, filepath):
        with open(filepath, 'w') as handle:
            json.dump(self.similarity, handle)

class RegressionRecommender(object):
    def __init__(self, feature_size=10, regressor=None):
        self.feature_size = feature_size
        self.user_svd = TruncatedSVD(n_components=feature_size)
        self.item_svd = TruncatedSVD(n_components=feature_size)
        if regressor is None:
            self.regressor = LinearRegression()

    def fit(self, rating):
        # rating (item x user)
        item_features = self.item_svd.fit_transform(rating)
        user_features = self.user_svd.fit_transform(rating.T)
        self.item_features = item_features
        self.user_features = user_features

        n_item, n_user = rating.shape
        n_examples = rating.count_nonzero()
        X = zeros((n_examples, self.feature_size + self.feature_size))
        y = zeros((n_examples, 1))
        for i, (item, user) in enumerate(zip(*rating.nonzero())):
            X[i] = concatenate([item_features[item], user_features[user]], axis=0)
            y[i] = rating[item, user]

        self.regressor.fit(X, y)
        return self

    def predict(self, item, user):
        user_features = self.user_features[user]
        item_features = self.item_features[item]

        input_features = concatenate(user_features, item_features)
        return self.regressor.predict(input_features)

    def save(self, filepath):
        to_save = {
            'regressor': self.regressor,
            'user_svd': self.user_svd,
            'item_svd': self.item_svd
        }
        with open(filepath, 'wb') as handle:
            saver = Pickler(handle, protocol=HIGHEST_PROTOCOL)
            saver.save(to_save)

    def load(self, filepath):
        with open(filepath, 'rb') as handle:
            loader = Unpickler(handle)
            state = loader.load()
            self.regressor = state['regressor']
            self.user_svd = state['user_svd']
            self.item_svd = state['item_svd']


class FactorizationRecommender(object):
    def __init__(self, feature_size=10):
        self.feature_size = feature_size
        self.fm = LightFM(no_components=feature_size)

    def fit(self, rating):
        self.fm.fit(rating.T)
        return self

    def predict(self, item, user):
        return self.fm.predict(user, item)

    def save(self, filepath):
        with open(filepath, 'wb') as handle:
            saver = Pickler(handle, protocol=HIGHEST_PROTOCOL)
            saver.save(self.fm)

class CfNadeRecommender(object):
    def __init__(self):
        pass

    def fit(self, rating):
        pass

    def predict(self, item, user):
        pass
