import pandas as pd 
from datetime import date
from os.path import exists
from datetime import datetime
from pandas.tseries.offsets import BusinessDay

import cira
from . import base 
from grazing.config import DATA_STORE_PATH

class BarsPipe(base.FeatruePipe):
 
    def transform(self, X: pd.DataFrame):
        pass


class BarsLoad(base.FeatureLoad):
    def __init__(self, symbol:str, start:date, end:date) -> None:
        self.symbol = symbol
        self.start = self.closest_business_day(start).date()
        self.end = self.closest_business_day(end).date()
        self.is_crypto = "/" in symbol

    def load(self) -> pd.DataFrame:
        global DATA_STORE_PATH
        file_path = DATA_STORE_PATH + f'/{self.symbol.replace("/", "_")}.csv'

        if self.is_crypto:
            ast = cira.Cryptocurrency(self.symbol)
        else: 
            ast = cira.Stock(self.symbol)

        if exists(file_path):
            df = ast.load_historical_data(file_path)
            print(f"{df.index[0].date()} == {self.start} and {df.index[-1].date()} == {self.end}")
            if df.index[0].date() == self.start and df.index[-1].date() == self.end:
                print("use all saved data")
                return df
            if df.index[0].date() != self.start: 
                print("bad start date")
                ast.save_historical_data(file_path, self.start, self.end)
                df = ast.load_historical_data(file_path)
                return df
            if df.index[-1].date() < self.end:  
                print("bad end date")
                start = datetime.fromisoformat(df.index[-1].isoformat()).date()
                new_df = ast.historical_data_df(start, self.end)
                df = pd.concat([df, new_df])
                df.to_csv(file_path)
                return df

        print("get all new data")
        df = ast.historical_data_df(self.start, self.end)
        df.to_csv(file_path)
        return df

