from operator import is_
import pandas as pd 
from datetime import date
from os.path import exists
from pathlib import Path
from datetime import datetime
import os 
from pandas.tseries.offsets import BusinessDay
from grazing.config import load_config
import cira
from . import base 

class BarsPipe(base.FeatruePipe): 
    def __init__(self, symbol:str, start:datetime, end:datetime, add_symbol_to_col:bool=True, data_store:str=".") -> None:
        super().__init__()
        self.symbol = symbol
        self.start = start.date()
        self.end = end.date()
        self.is_crypto = "/" in symbol
        self.add_symbol_to_col = add_symbol_to_col
        self.data_store = load_config("./config.yaml")["settings"]["data_store_path"]

    def transform(self, X: pd.DataFrame):
        df = self.load()
        df.drop(columns=["symbol"], inplace=True)
        return pd.concat([X, df], axis=1)

    def load(self) -> pd.DataFrame:
        if not Path(self.data_store).is_dir():
            os.system(f"mkdir {self.data_store}")
        file_path = self.data_store + f'/{self.symbol.replace("/", "_")}.csv'

        if self.is_crypto:
            ast = cira.Cryptocurrency(self.symbol)
        else: 
            ast = cira.Stock(self.symbol)

        if exists(file_path):
            df = ast.load_historical_data(file_path)
            if df.index[0].date() == self.start and df.index[-1].date() == self.end:
                return df
            if df.index[0].date() != self.start: 
                ast.save_historical_data(file_path, self.start, self.end)
                df = ast.load_historical_data(file_path)
                return df
            if df.index[-1].date() < self.end:  
                start = datetime.fromisoformat(df.index[-1].isoformat()).date()
                new_df = ast.historical_data_df(start, self.end)
                df = pd.concat([df, new_df])
                df.to_csv(file_path)
                return df

        df = ast.historical_data_df(self.start, self.end)
        df.to_csv(file_path)
        return df


class PricePipe(base.FeatruePipe):
    
    def __init__(self, symbol:str, column_as_price:str="close", is_symbol_in_col:bool=True) -> None:
        super().__init__()
        self.column_as_price = column_as_price
        self.symbol = symbol
        self.is_symbol_in_col = is_symbol_in_col

    def transform(self, X: pd.DataFrame):
        if not self.is_symbol_in_col: 
            return X[self.column_as_price].to_frame()
         
        for col_name in X.keys():
            if self.column_as_price in col_name: 
                X[self.symbol] = X[col_name]
        return X.drop(columns=[col_name for col_name in X.keys() if self.symbol in col_name and col_name != self.symbol])    
        

