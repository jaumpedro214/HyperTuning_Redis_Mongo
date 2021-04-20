import redis

def insert_requisition( redis_client, hname, params ):
    for key, value  in params.items():
        redis_client.hset(hname, key, value)
    
    redis_client.lpush('requisitions-list',hname)


redis_client = redis.Redis()

models = [('10', {"name":"RandomForestRegressor", 
                  "base":"iris",
                  "min_samples_split":10, "min_impurity_decrease":1.0000 , 
                  "metrics":"neg_mean_absolute_error"}),
          ('11', {"name":"RandomForestRegressor",
                  "base":"iris", 
                  "n_estimators":200, "min_samples_split":4, "criterion":"mse", 
                  "metrics":"neg_mean_squared_error,r2"}),
          ('12', {"name":"Ridge",
                  "base":"iris", 
                  "alpha":0.5, "tol":0.0001,
                  "metrics":"r2"
                   })]

for model in models:
    print(model[0], model[1])
    insert_requisition( redis_client, model[0], model[1] )