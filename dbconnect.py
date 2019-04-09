from pymongo import MongoClient
import yaml

with open("config.yaml", "r") as ymlfile:
    cfg = yaml.load(ymlfile)

client = MongoClient(cfg['mongodb']['client'])
