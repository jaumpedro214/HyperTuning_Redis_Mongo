import redis
import numpy as np
import pymongo

# Models supported
from sklearn.svm import SVR, SVC
from sklearn.linear_model import LinearRegression, Ridge, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

# Get evaluation metrics
from sklearn.metrics import get_scorer
from sklearn.metrics import SCORERS

# Datasets available
from sklearn.datasets import make_regression, load_boston, load_diabetes
from sklearn.datasets import make_classification, load_iris, load_breast_cancer
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.preprocessing import label_binarize
import numpy as np

from pprint import pprint
import datetime

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

def get_model(name):
    # Sklearn models mapped by name
    models = { "LinearRegression":LinearRegression(),
               "Ridge":Ridge(),
               "RandomForestRegressor":RandomForestRegressor(),
               "RandomForestClassifier":RandomForestClassifier(),
               "LogisticRegression":LogisticRegression(),
               "SVR":SVR(),
               "SVC":SVC(),
                }
    return models[name]

def train_model(model, metrics, base):
    X, y = datasets[base]

    scorers = dict()
    for metric in metrics:
        scorers[metric] = metric

    # Cross validation cv = 3
    cvs = cross_validate(model, X, y, return_train_score=True,
                         scoring=scorers, cv=4)

    # Mean of each score list
    cvs_means = { key:np.mean(value) for key,value in cvs.items() }

    return cvs_means

def process_model( params ):
    assert type(params) == dict
    if params == {}:
        print("Warning: Params dictonary is empty, returning")
        return
    
    name = params['name']
    base = params['base']
    metrics = set(params['metrics'].split(','))

    del params['name']
    del params['base']
    del params['metrics']

    # Setting ML model
    model = get_model(name)

    # Setting model parameters
    for key, value in params.items():
        params[key] = convert_string(value)
    model.set_params(**params)

    # Training/evaluate model
    scores = train_model(model, metrics, base)

    # Building MongoDB entry
    mongo_doc = {"name":name,
                 "params":model.get_params(),
                 "database":base,
                 "scores":scores,
                 "date":datetime.datetime.now()
                }
    return (mongo_doc)


# Available Datasets
datasets = {"diabetes":load_diabetes(return_X_y=True),
            "boston":load_boston(return_X_y=True),
            "iris":load_iris(return_X_y=True),
            "breast_cancerd":load_breast_cancer(return_X_y=True)
            }

# Connecting to redis client
r = redis.Redis(decode_responses=True)

# Connecting to mongo client
m = pymongo.MongoClient('localhost',27017)

while True:
    
    id_requisicao = r.brpop('requisitions-list', 5*60 )
    if id_requisicao == None:
        print("Shutdown...")
        break
    id_requisicao = id_requisicao[1]
    
    params = r.hgetall(id_requisicao)
    print(f"Requisition - {id_requisicao} - {params['name']}")
    m_db = m.mongo_db
    c_db = m_db.doc_table
    resultado = c_db.insert_one(process_model( params ))
    r.delete(id_requisicao)