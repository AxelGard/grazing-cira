import time 
import datetime
import logging
import cira 

from grazing.features.bars import BarsLoad
from datetime import datetime

def main():
    cira.auth.KEY_FILE = "../alpc_key.json"
    assert cira.auth.check_keys(), "the set keys dose not work"
    start = datetime(2021, 1, 1).date()
    end   = datetime(2023, 1, 1).date()
    bar = BarsLoad("BTC/USD", start, end)
    df = bar.load()
    print(df)

if __name__ == "__main__":
    main()
