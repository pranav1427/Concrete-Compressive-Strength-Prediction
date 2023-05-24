import pymongo
import pandas as pd
import json
# Provide the mongodb localhost url to connect python to mongodb.
client = pymongo.MongoClient("mongodb://localhost:27017/neurolabDB")

DATA_FILE_PATH="/config/workspace/concrete_data.csv"
DATABASE_NAME="concrete_data"
COLLECTION_NAME="concrete_strength"


if __name__=="__main__":
    df=pd.read_csv(DATA_FILE_PATH)
    print(f"Rows and Columns: {df.shape}")

    #converting dataframe to json to dump record in mongo db
    df.reset_index(drop=True,inplace=True)

    json_record= list(json.loads(df.T.to_json()).values())
    print(json_record[0])

    #inserting converted json record to mongo db
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)
