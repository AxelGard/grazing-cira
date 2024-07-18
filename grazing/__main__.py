import datetime
import logging
from datetime import datetime, timedelta
from sklearn.pipeline import Pipeline
import pandas as pd 
import numpy as np
import cira 
import pickle
from grazing.strategies import load_startegy
from grazing.strategies.bollinger_bands import BollingStartegy
from grazing.features import collect_features, collect_prices
from grazing.features.bars import BarsPipe, PricePipe
from grazing.config import config, load_config

log = logging.getLogger(__name__)


def trade(strat:cira.strategy.Strategy,feature_data: pd.DataFrame, asset_prices: pd.DataFrame):
    exchange = cira.Exchange()
    if not exchange.is_open(): 
        log.warn("Exchange was not open")
        return
    portfolio = cira.Portfolio()
    cash = portfolio.cash()
    symbols = config["trading"]["symbols"]

    stk_q = [cira.purtfolio.get_allocation(sym) for sym in symbols]
    positions_changes = strat.iterate(feature_data, asset_prices, np.array(stk_q), cash)

    for i in range(len(positions_changes)): 
        symbol = symbols[i]
        stk = cira.Stock(symbol)
        pos = positions_changes[i]
        log.info(f"new position size: {pos} of symbol {symbol}")
        if pos < 1 and stk_q > 1: 
            if stk_q <= abs(pos):
                pos = stk_q
            stk.sell(pos)
        elif pos > 1:
            stk.buy(pos)  

def run():
    global config
    config = load_config("./config.yaml")
    strat = load_startegy("/home/axel/Programs/repositories/grazing-cira/grazing/strategies/bollinger_bands.pkl")

    start = datetime(config["trading"]["features"]["start_date"])
    end   = datetime.today() - timedelta(days=1) 

    symbols = config["trading"]["symbols"]
    prices = collect_prices(symbols=symbols, start=start, end=end)

    pipes = config["trading"]["features"]["pipe"]
    features = collect_features(pipes=pipes, symbols=symbols, start=start, end=end)

    trade(strat=strat, feature_data=features, asset_prices=prices)


def main_prod():
    global config
    config = load_config("./config.yaml")

    cira.auth.KEY_FILE = config["alpaca"]["key_file"]
    assert cira.auth.check_keys(), "set alpaca keys did not work"

    scheduler = cira.strategy.Scheduler()
    scheduler.clear_all_jobs()
    scheduler.add_daily_job_at(run, config["settings"]["local_exec_time"])
    log.debug(scheduler.get_all_jobs())
    scheduler.run() # this runs forever, it will just keep on waiting for the time to match

def main_debug():
    global config
    config = load_config("./config.yaml")

    cira.auth.KEY_FILE = config["alpaca"]["key_file"]
    assert cira.auth.check_keys(), "set alpaca keys did not work"

    print("Got config")
    strat = cira.strategy.Strategy.load("/home/axel/Programs/repositories/grazing-cira/grazing/strategies/bollinger_bands.pkl")
    print(strat.risk)
    print() 
    start =  datetime.strptime(config["trading"]["features"]["start_date"], "%Y-%m-%d")
    end   = datetime.today() - timedelta(days=1) 

    symbols = config["trading"]["symbols"]
    prices = collect_prices(symbols=symbols, start=start, end=end)

    pipes = config["trading"]["features"]["pipe"]
    features = collect_features(pipes=pipes, symbols=symbols, start=start, end=end)
    print(features)

if __name__ == "__main__":
    main_debug()
