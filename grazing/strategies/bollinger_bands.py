from numpy import ndarray
from pandas import DataFrame
import cira 

from cira.strategy import back_test
import numpy as np


class BollingStartegy(cira.strategy.Strategy):

    def __init__(self, sma_window = 20, standard_deviation = 2, risk=0.1) -> None:
        super().__init__(name="Bolling")
        self.sma_window = sma_window
        self.standard_deviation = standard_deviation
        self.risk = risk 
        self.allocation = []

    def iterate(self, feature_data: DataFrame, prices: DataFrame, portfolio: ndarray, cash:float)-> ndarray: 
        _feature_data = feature_data.copy()
        _feature_data["sma"] = _feature_data["open"].rolling(window=self.sma_window).mean() # simple moving avrage 
        _feature_data["sd"] =  _feature_data["open"].rolling(window=self.sma_window).std()

        _feature_data["ub"] =  _feature_data["sma"] + self.standard_deviation * _feature_data["sd"]
        _feature_data["lb"] =  _feature_data["sma"] - self.standard_deviation * _feature_data["sd"]

        _all = np.array([0])
        if len(_feature_data) < self.sma_window:
            pass 

        elif prices.iloc[-1].values[0] >= _feature_data.iloc[-1]["ub"]:
            _all = np.array([-1*portfolio[-1]*self.risk])

        elif prices.iloc[-1].values[0] <= _feature_data.iloc[-1]["lb"]:
            _all = np.array([int((cash*self.risk))//prices.iloc[-1].values[0]])

        self.allocation.append(_all)
        return _all.astype(float)
                


    def fit(self, featrue_data: DataFrame, sma_windows = [10, 20, 30], standard_deviations = [1,2,3], risk_lvls=[0.1, 0.2, 0.3], capital=10_000):
        best_prof = 0 
        best_sma = 20
        best_std = 2
        risk = 0.1
        for r in risk_lvls:
            for sma_w in sma_windows: 
                for std in standard_deviations: 
                    strat = BollingStartegy(sma_w, std, risk=r)
                    bt = back_test(strat, featrue_data, featrue_data["close"].to_frame(), capital) 
                    prof = bt[strat.name].values[-1] - capital 
                    if prof > best_prof: 
                        best_sma = sma_w
                        best_std = std
                        best_prof = prof
                        risk = r

        print(f"sma:{best_sma}, std:{best_std} @ risk {risk}, portfolio change {best_prof:.2f}$")

        self.sma_window = best_sma
        self.standard_deviation = best_std
        self.risk = risk
        return self
                

    def collect_feature(self):
        pass 