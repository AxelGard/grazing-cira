import cira
from grazing.strategies.bollinger_bands import BollingStartegy
import logging
from typing import Union

__strat_log = logging.getLogger(__name__)

def load_startegy(strategy_name:str) -> Union[None,cira.strategy.Strategy]:
    global avilabel_strategies, log
    if not strategy_name in avilabel_strategies.keys():
        __strat_log.critical(f"given strategy name ({strategy_name}) has not been setup")
        return None
    return avilabel_strategies[strategy_name]()


avilabel_strategies = {
    "bolling": BollingStartegy,
    "random": cira.strategy.Randomness,
    "byandhold": cira.strategy.ByAndHold,
    "dollarcostaverageing": cira.strategy.DollarCostAveraging,

}