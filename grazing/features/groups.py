from sklearn.pipeline import Pipeline
from datetime import datetime
import pandas as pd 

from grazing.features.bars import BarsPipe, PricePipe
from grazing.features.techniacal_analysis import MovingAvrage, RelativeStrengthIndex, BollingerBands
from grazing.features.util import AddSymbolToColumns 

def feature_group_simple(symbol:str, start:datetime, end:datetime) -> pd.DataFrame:  
    return [
        ("bars", BarsPipe(symbol=symbol, start=start, end=end)),
    ]


def feature_group_basic_techincal_analysis(symbol:str, start:datetime, end:datetime) -> pd.DataFrame:  
    return [
        ("bars", BarsPipe(symbol=symbol, start=start, end=end)),
        ("rsi", RelativeStrengthIndex()),
        ("bollinger", BollingerBands()),
    ] + [(f"{i}sma", MovingAvrage(i, "open")) for i in [10, 50, 100]]


