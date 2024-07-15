from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class FeatruePipe(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X:pd.DataFrame):
        raise NotImplementedError

