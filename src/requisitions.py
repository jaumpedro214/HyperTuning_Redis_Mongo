import redis
import uuid

from sklearn.model_selection import ParameterGrid

def insert_requisition( redis_client, params ):
    hname = str(uuid.uuid1()) # Creating UUID
    print(hname)
    for key, value  in params.items():
        redis_client.hset(hname, key, value)
    
    redis_client.lpush('requisitions-list',hname)


redis_client = redis.Redis()
# Regression
param_grind_forr = {'max_depth': [None, 10, 40, 50], 'max_leaf_nodes': [None, 40], 
                    'min_impurity_decrease': [0.0, 0.1], 
                    'min_samples_leaf': [1, 2, 4], 'min_samples_split': [2, 8],  
                    'n_estimators':[1, 10, 100, 500],
                    'base':['boston', 'diabetes'],
                    'metrics':['r2,neg_mean_squared_error,neg_mean_absolute_percentage_error']
                    }
param_grid_ridge = {'alpha': [0.001, 0.1, 1.0, 10, 100], 
                    'fit_intercept': [False, True], 
                    'normalize': [False, True], 
                    'tol': [1e-3, 1e-2],
                    'base':['boston', 'diabetes'],
                    'metrics':['r2,neg_mean_squared_error,neg_mean_absolute_percentage_error']
                    }
params_grid_svr = {'C': [0.001, 0.1, 1.0, 10, 100],
                   'kernel': ['linear', 'poly', 'rbf'], 
                   'max_iter': [-1, 100], 'tol': [1e-3, 1e-2],
                   'base':['boston', 'diabetes'],
                   'metrics':['r2,neg_mean_squared_error,neg_mean_absolute_percentage_error']
                    }

# Classification
params_grid_log = {'C': [0.001, 0.1, 1.0, 10, 100], 'fit_intercept':[True, False], 
                   'max_iter': [10, 100, 500], 'multi_class':['auto'], 
                   'penalty':['l1', 'l2', 'elasticnet'],
                   'base':['iris', 'breast_cancer'],
                   'metrics':['roc_auc,accuracy,f1_micro']
                   }
params_grid_for = {'max_depth': [None, 10, 40, 50], 'max_leaf_nodes': [None, 40], 
                   'min_impurity_decrease': [0.0, 0.1], 
                   'min_samples_leaf': [1, 2, 4], 'min_samples_split': [2, 8],  
                   'n_estimators':[1, 10, 100, 500],
                   'base':['iris', 'breast_cancer'],
                   'metrics':['roc_auc,accuracy,f1_micro']
                   }
params_grid_svc = {'C': [0.001, 0.1, 1.0, 10, 100],
                   'kernel': ['linear', 'poly', 'rbf'], 
                   'max_iter': [-1, 100], 'tol': [1e-3, 1e-2],
                   'base':['iris', 'breast_cancer'],
                   'metrics':['roc_auc,accuracy,f1_micro']
                   }
models = []
models.extend(list(ParameterGrid(param_grind_forr)))
models.extend(list(ParameterGrid(param_grid_ridge)))
models.extend(list(ParameterGrid(params_grid_svr)))
models.extend(list(ParameterGrid(params_grid_log)))
models.extend(list(ParameterGrid(params_grid_for)))
models.extend(list(ParameterGrid(params_grid_svc)))

for model in models:
    insert_requisition( redis_client, model )