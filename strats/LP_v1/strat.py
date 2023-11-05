from utils import *
from pulp import *
import warnings
warnings.filterwarnings('always')
warnings.filterwarnings('ignore')
from importlib import import_module

def compute_strat(strat_params):
    prob=LpProblem('portfolio',LpMaximize)
    vars=LpVariable.dicts("value",range(strat_params["N"]),0,200,cat="Integer")
    
    stats=[]
    #construct cost::
    strat_params["cost"]=yf.get_curr_cost(strat_params["symbols"])
    for i in range(strat_params["N"]):
        sym=strat_params["symbols"][i]
        dat=yf.get_open_close_with_time(sym,strat_params["h_time"][i])
        
        stats.append(pred_return(get_distri(dat)))
    
    prob+=(lpSum(vars[i]*strat_params["cost"][i]*np.power(stats[i]["variance"],0.5) for i in range(strat_params["N"]))<=strat_params["risk"])
    
    prob+=(lpSum(vars[i]*strat_params["cost"][i] for i in range(strat_params["N"]))<=strat_params["inv_limit"])

    prob+=(lpSum(vars[i]*strat_params["cost"][i]*stats[i]["mean"] for i in range(strat_params["N"])))
    
    prob.solve()

    #check if there is indeed a solution::

    return [vars[i].value() for i in range(strat_params["N"])]


def run_strat_v1(cfg_file):
    #reads the cfg file and runs the strat using compute_strat
    
    params=import_module("cfg."+cfg_file).cfg
 

    alphas=compute_strat(params)

    #execute the strat
    print(alphas)

if __name__=="__main__":

    run_strat_v1("cfg1")