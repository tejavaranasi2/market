from utils import *
import cvxpy as cp
import warnings
warnings.filterwarnings('always')
warnings.filterwarnings('ignore')
from importlib import import_module

def compute_strat(strat_params):
    
    vars=cp.Variable((strat_params["N"],1),nonneg=True)
    stats=[]
    #construct cost::
    strat_params["cost"]=yf_eq.get_curr_cost(strat_params["symbols"])
    tot_data=[]
    for i in range(strat_params["N"]):
        sym=strat_params["symbols"][i]
        dat=yf_eq.get_open_close_with_time(sym,strat_params["h_time"][i])
        tot_data.append(get_reuturn_data(dat))
        stats.append(pred_return(get_distri(dat),yf_opt.options_chain(sym)))
    
    cov=get_cov_matrix(tot_data)
    ret_arr=np.array([[strat_params["cost"][i]*stats[i]["mean"]] for i in range(strat_params["N"])])
    pr_arr=np.array([[strat_params["cost"][i]] for i in range(strat_params["N"])])

    objective=cp.Maximize(ret_arr.T@vars)
    

    constraints=[cp.quad_form(vars,cov) <=strat_params["risk"],pr_arr.T@vars<=strat_params["inv_limit"]]
    
    prob=cp.Problem(objective,constraints)
    prob.solve()

    #check if there is indeed a solution::
   
    return [vars[i].value[0] for i in range(strat_params["N"])]


def run_strat_v1(cfg_file):
    #reads the cfg file and runs the strat using compute_strat
    
    params=import_module("cfg."+cfg_file).cfg
 
    
    alphas=compute_strat(params)

    #execute the strat
    print(alphas)

if __name__=="__main__":
    #plot_option_data('DIS')
    run_strat_v1("cfg2")