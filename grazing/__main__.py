import datetime
import logging
from datetime import datetime
import pandas as pd 
import numpy as np
import cira 
from grazing.strategies import load_startegy
from grazing.features import collect_features, collect_prices
from grazing.config import config, load_config
from grazing.strategies import * # BUG: all stat classes needs to be in this scope for pkl to load file

log = logging.getLogger(__name__)


def trade(strat:cira.strategy.Strategy, feature_data: pd.DataFrame, asset_prices: pd.DataFrame):
    exchange = cira.Exchange()
    if not exchange.is_open(): 
        log.warning("Exchange was not open")
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
        print(f"new position size: {pos} of symbol {symbol}") 
        if pos < 0.0 and stk_q > 1: 
            if stk_q <= abs(pos):
                pos = stk_q
            stk.sell(pos)
        elif pos > 0.0:
            stk.buy(pos)  

def run():
    global config
    config = load_config("./config.yaml")
    strat = load_startegy(config["trading"]["strategy"])

    start =  datetime.strptime(config["trading"]["features"]["start_date"], "%Y-%m-%d")
    end   = datetime.today() 

    symbols = config["trading"]["symbols"]
    prices = collect_prices(symbols=symbols, start=start, end=end)

    pipe = config["trading"]["features"]["pipe"]
    features = collect_features(pipe=pipe, symbols=symbols, start=start, end=end)

    trade(strat=strat, feature_data=features, asset_prices=prices)


def main_prod():
    global config
    config = load_config("./config.yaml")

    logging.basicConfig(
        filename=".grazing.log",
        encoding="utf-8",
        filemode="a",
        format="{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
        level=logging.INFO
    )

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
    logging.basicConfig(
        datefmt="%Y-%m-%d %H:%M",
        level=logging.DEBUG
    )

    cira.auth.KEY_FILE = config["alpaca"]["key_file"]
    assert cira.auth.check_keys(), "set alpaca keys did not work"

    start = datetime.strptime(config["trading"]["features"]["start_date"], "%Y-%m-%d")
    end   = datetime.today() 

    symbols = config["trading"]["symbols"]
    prices = collect_prices(symbols=symbols, start=start, end=end)

    pipe = config["trading"]["features"]["pipe"]
    features = collect_features(pipe=pipe, symbols=symbols, start=start, end=end)

    strat = load_startegy(config["trading"]["strategy"])
    run() 


if __name__ == "__main__":
    main_debug()
