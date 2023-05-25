import pymongo
import pandas as pd 
import json
from dataclasses import dataclass
import os

# provide mongodb local host to connect python to mongodb

@dataclass
class EnvironmentVariable:
    mongo_db_url:str=os.getenv("MONDO_DB_URL")

env_var= EnvironmentVariable()

mongo_client=pymongo.MongoClient(env_var.mongo_db_url)