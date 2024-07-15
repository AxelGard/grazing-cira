import yaml
import logging


log = logging.getLogger(__name__)
config = {}

def load_config(path="./config.yaml") -> dict:
    with open(path, 'r') as file:
        conf = yaml.safe_load(file)
    if not conf: 
        log.critical(f"Was not able to load config path={path}, read: {conf}")
        return dict()
    return dict(conf)