import cira
from grazing.strategies.bollinger_bands import BollingStartegy


def load_startegy(file_path:str):
    return cira.strategy.Strategy.load(file_path=file_path)