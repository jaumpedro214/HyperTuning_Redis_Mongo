import redis

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import get_scorer
from sklearn.metrics import SCORERS

from pprint import pprint

# Sklearn models mapped by name
models = { "LinearRegression":LinearRegression(),
           "Ridge":Ridge(),
           "RandomForestRegressor":RandomForestRegressor() }
           

# Function to convert string into int, float, string
def convert_string(s):
    assert type(s) == str
    try:
        s=int(s)
    except ValueError:
        try:
            s=float(s)
        except ValueError:
            pass
    return s

def train_model( params ):

    assert type(params) == dict
    if params == {}:
        print("Warning: Params dictonary is empty, returning")
        return
    
    name = params['name']
    base = params['base']
    metrics = params['metrics'].split(',')

    del params['name']
    del params['base']
    del params['metrics']

    print( f"Training {name} on base {base}" )

    # Setting ML model 
    model = models[name]

    # Setting model parameters
    for key, value in params.items():
        params[key] = convert_string(value)
    model.set_params(**params)

    print( f"Evaluating with {metrics}" )
    
    # Getting scorers (metrics) objects
    scorers = []
    for metric in metrics:
        scorers.append( get_scorer(metric) )

    pprint( model )
    print(" ")
    
# Connecting to redis client
r = redis.Redis(decode_responses=True)

while True:
    
    id_requisicao = r.brpop('requisitions-list', 10)
    if id_requisicao == None:
        print("Shutdown...")
        break
    id_requisicao = int(id_requisicao[1])

    print(f"Atendendo à requisição {id_requisicao}")
    params = r.hgetall(id_requisicao)
    train_model( params )
    r.delete(id_requisicao)