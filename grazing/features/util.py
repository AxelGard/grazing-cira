from grazing.features.base import FeatruePipe
import pandas as pd 


class AddSymbolToColumns(FeatruePipe):
    def __init__(self, symbol:str) -> None:
        self.symbol = symbol

    def transform(self, X: pd.DataFrame): 
        for i, col_name in enumerate(X.keys()):
            X.columns.values[i] = f"{self.symbol}_{col_name}"
        return X