import redis
import uuid

def insert_requisition( redis_client, params ):
    hname = str(uuid.uuid1()) # Creating UUID
    print(hname)
    for key, value  in params.items():
        redis_client.hset(hname, key, value)
    
    redis_client.lpush('requisitions-list',hname)


redis_client = redis.Redis()

models = [{"name":"RandomForestRegressor", 
           "base":"boston",
           "min_samples_split":10, "min_impurity_decrease":1.0000, 
           "metrics":"neg_mean_absolute_error"},
          {"name":"RandomForestRegressor",
           "base":"boston", 
           "n_estimators":200, "min_samples_split":4, "criterion":"mse", 
           "metrics":"neg_mean_squared_error,r2"},
          {"name":"Ridge",
           "base":"boston", 
           "alpha":0.5, "tol":0.001,
           "metrics":"r2"}
           ]

for model in models:
    insert_requisition( redis_client, model )