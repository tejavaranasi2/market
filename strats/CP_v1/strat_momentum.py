from utils import *
import cvxpy as cp
import warnings
warnings.filterwarnings('always')
warnings.filterwarnings('ignore')
from importlib import import_module

def compute_momentum(strat_params):
    vars=cp.Variable((strat_params["N"],1))
    stats=[]
    #construct cost::
    strat_params["cost"]=yf_eq.get_curr_cost(strat_params["symbols"])
    tot_data=[]
    for i in range(strat_params["N"]):
        sym=strat_params["symbols"][i]
        dat=yf_eq.get_open_close_with_time(sym,strat_params["h_time"][i])
        tot_data.append(get_reuturn_data(dat))
        stats.append(pred_return(get_distri(dat),yf_opt.options_chain(sym)))
    
   
    ret_arr=np.array([[strat_params["cost"][i]*stats[i]["mean"]] for i in range(strat_params["N"])])
    pr_arr=np.array([[strat_params["cost"][i]] for i in range(strat_params["N"])])

    objective=cp.Maximize(ret_arr.T@vars)
    

    constraints=[]
    for i in range(strat_params["N"]):
        constraints.append(vars[i]>=0)

    prob=cp.Problem(objective,constraints)
    prob.solve()

    #check if there is indeed a solution::
    rounded=[custom_rounding(vars[i].value[0],2) for i in range(strat_params["N"])]
    org=[vars[i].value[0] for i in range(strat_params["N"])]
    app=(ret_arr.T@np.array(rounded))/(ret_arr.T@np.array(org))
    return rounded,app
