import redis

def train_model( params ):
    if params == {}:
        print("Empty params!")
        return
    
    name = params[b'name']
    base = params[b'base']
    metrics = params[b'metrics']
    del params[b'name']
    del params[b'base']
    del params[b'metrics']
    print( f"Treinando {name} na base {base}" )
    print( f"Avaliando com as métricas {metrics}" )
    print( params )


redis_client = redis.Redis()

while True:
    id_requisicao = int( redis_client.brpop('requisitions-list')[1] )
    print(f"Atendendo à requisição {id_requisicao}")
    train_model( redis_client.hgetall(id_requisicao) )
    redis_client.delete(id_requisicao)
