from sklearn.pipeline import Pipeline
from datetime import datetime 
import pandas as pd 

from grazing.features.bars import BarsPipe, PricePipe
from grazing.features.util import AddSymbolToColumns 
from grazing.features.groups import feature_group_simple, feature_group_basic_techincal_analysis


def collect_prices(symbols:list[str], start:datetime, end:datetime) -> pd.DataFrame:
    bars = pd.DataFrame()
    bars_pipe = Pipeline([(f"bars_{sym}", BarsPipe(symbol=sym, start=start, end=end)) for sym in symbols])
    bars = bars_pipe.fit_transform(bars)
    prices_pipe =  Pipeline([(f"bars_{sym}", PricePipe(sym, "close")) for sym in symbols])
    return prices_pipe.fit_transform(bars)

def collect_features(pipes:list[str], symbols:list[str], start:datetime, end:datetime) -> pd.DataFrame:
    features = []
    for p in pipes: 
        for sym in symbols:
            features += availabel_pipes[p](symbol=sym, start=start, end=end) 

    pipe = Pipeline(features) 
    return pipe.fit_transform(pd.DataFrame())



availabel_pipes = {
    "simple": feature_group_simple, 
    "technical": feature_group_basic_techincal_analysis
}
