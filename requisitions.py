import redis

def insert_requisition( redis_client, hname, params ):
    for key, value  in params.items():
        redis_client.hset(hname, key, value)
    
    redis_client.lpush('requisitions-list',hname)


redis_client = redis.Redis()

models = [('10', {"name":"RandomForest", "ntrees":500, "max":20, "metrics":"accuracy", "base":"iris"}),
          ('11', {"name":"RandomForest", "ntrees":200, "max":20, "metrics":"ABC", "base":"iris"}),
          ('12', {"name":"RandomForest", "ntrees":100, "max":15, "metrics":"accuracy", "base":"iris"})]

for model in models:
    print(model[0], model[1])
    insert_requisition( redis_client, model[0], model[1] )