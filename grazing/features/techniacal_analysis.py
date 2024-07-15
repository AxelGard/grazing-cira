from pandas import DataFrame
from grazing.features.base import FeatruePipe


class MovingAvrage(FeatruePipe):
    def __init__(self, window_size:int=30, on_column="open") -> None:
        super().__init__()
        self.window_size = window_size
        self.on_column = on_column

    def transform(self, X: DataFrame):
        assert self.on_column in X.keys(), f"Moving Avrage, needs {self.on_column} to be in X"
        X[f"{self.window_size}_sma"] = X[self.on_column].rolling(window=self.window_size).mean()
        return X


class RelativeStrengthIndex(FeatruePipe):
    def __init__(self, window_size:int=20, on_column="open") -> None:
        super().__init__()
        self.window_size = window_size
        self.on_column = on_column

    def transform(self, X: DataFrame):
        assert self.on_column in X.keys(), f"RSI, needs {self.on_column} to be in X"
        delta = X["open"].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta<0,0)
        avg_gain = gain.rolling(self.window_size).mean()
        avg_loss = loss.rolling(self.window_size).mean() 
        X["rsi"] = 100 - (100 / (1 + (avg_gain / avg_loss)))
        return X


class BollingerBands(FeatruePipe):
    def __init__(self, window_size:int=20, on_column:str="open", number_of_standard_deviations:int=2) -> None:
        super().__init__()
        self.window_size = window_size
        self.on_column = on_column
        self.n_std = number_of_standard_deviations

    def transform(self, X: DataFrame):
        X["sma"] = X[self.on_column].rolling(window=self.window_size).mean() # simple moving avrage 
        X["sd"]  = X[self.on_column].rolling(window=self.window_size).std()
        X["ub"] = X["sma"] + self.n_std * X["sd"]
        X["lb"] = X["sma"] - self.n_std * X["sd"]
        return X