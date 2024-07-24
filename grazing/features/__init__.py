from sklearn.pipeline import Pipeline
from datetime import datetime 
import pandas as pd 

from grazing.features.groups import feature_group_simple, feature_group_basic_techincal_analysis, feature_group_price


def collect_features(pipe:str, symbols:list[str], start:datetime, end:datetime) -> pd.DataFrame:
    result = pd.DataFrame()
    for sym in symbols:
        features = availabel_pipes[pipe](symbol=sym, start=start, end=end) 
        __pipe = Pipeline(features) 
        fited = __pipe.fit_transform(pd.DataFrame())
        result = pd.concat([result, fited], axis=1)
        del __pipe
    return result


availabel_pipes = {
    "bars": feature_group_simple, 
    "technical": feature_group_basic_techincal_analysis,
    "price": feature_group_price,
}
