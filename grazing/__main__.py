import datetime
import logging
import cira 

from grazing.features.bars import BarsPipe, PricePipe
from datetime import datetime, timedelta
from sklearn.pipeline import Pipeline
import pandas as pd 

def main():
    cira.auth.KEY_FILE = "../alpc_key.json"
    assert cira.auth.check_keys(), "the set keys dose not work"

    start = datetime(2021, 1, 1)
    end   = datetime.today() - timedelta(days=1) 
    symbols = ["AAPL", "MSFT", "AMZN", "INTC", "GOOGL"] 

    bars = pd.DataFrame()
    bars_pipe = Pipeline([(f"bars_{sym}", BarsPipe(sym, start, end)) for sym in symbols])
    bars = bars_pipe.fit_transform(bars)

    prices_pipe =  Pipeline([(f"bars_{sym}", PricePipe(sym, "close")) for sym in symbols])
    prices = prices_pipe.fit_transform(bars)
    print(prices)
    

if __name__ == "__main__":
    main()
