from grazing.features.base import FeatruePipe
import pandas as pd 
import typing


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


class DropNa(FeatruePipe):
    def transform(self, X: pd.DataFrame):
        return X.dropna()


class SelectColumn(FeatruePipe):
    def __init__(self, column:str, change_name_to:typing.Union[str, None]=None) -> None:
        self.column = column
        self.change_name_to = change_name_to

    def transform(self, X: pd.DataFrame): 
        if self.change_name_to == None: 
            return X[self.column].to_frame()
        df = pd.DataFrame()
        df[self.change_name_to] = X[self.column]
        return df