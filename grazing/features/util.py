from grazing.features.base import FeatruePipe
import pandas as pd 


class AddSymbolToColumns(FeatruePipe):
    def __init__(self, symbol:str) -> None:
        self.symbol = symbol

    def transform(self, X: pd.DataFrame): 
        for i, col_name in enumerate(X.keys()):
            X.columns.values[i] = f"{self.symbol}_{col_name}"
        return X


class FillNa(FeatruePipe):
    def __init__(self, fill_with = 0) -> None:
        self.fill_with = fill_with

    def transform(self, X: pd.DataFrame):
        return X.fillna(self.fill_with)