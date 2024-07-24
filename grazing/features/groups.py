from sklearn.pipeline import Pipeline
from datetime import datetime
import pandas as pd 

from grazing.features.bars import BarsPipe, PricePipe
from grazing.features.techniacal_analysis import MovingAvrage, RelativeStrengthIndex, BollingerBands
from grazing.features.util import AddSymbolToColumns, FillNa, DropNa, SelectColumn

def feature_group_simple(symbol:str, start:datetime, end:datetime) -> list:  
    return [
        (f"bars_{symbol}", BarsPipe(symbol=symbol, start=start, end=end)),
    ]


def feature_group_basic_techincal_analysis(symbol:str, start:datetime, end:datetime) -> list:  
    return [
        ("bars", BarsPipe(symbol=symbol, start=start, end=end)),
        ("rsi", RelativeStrengthIndex()),
        ("bollinger", BollingerBands()),
    ] + [(f"{i}sma", MovingAvrage(i, "open")) for i in [10, 50, 100]] + [
        ("fillna", FillNa(0))
    ]


def feature_group_price(symbol:str, start:datetime, end:datetime) -> list:  
    return [    
        (f"bars_{symbol}", BarsPipe(symbol=symbol, start=start, end=end, add_symbol_to_col=True)),
        (f"select_{symbol}", SelectColumn(column="close", change_name_to=symbol)),
    ]
