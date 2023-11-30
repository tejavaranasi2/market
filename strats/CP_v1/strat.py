from utils import *
import cvxpy as cp
import warnings
warnings.filterwarnings('always')
warnings.filterwarnings('ignore')
from importlib import import_module

def compute_strat(strat_params,use_opt=False):
    
    vars=cp.Variable((strat_params["N"],1))
    stats=[]
    #construct cost::
    strat_params["cost"]=[]
    #strat_params["cost"]=yf_eq.get_curr_cost(strat_params["symbols"])
    tot_data=[]
    fin_price=[]
    for i in range(strat_params["N"]):
        sym=strat_params["symbols"][i]
        dat=yf_eq.get_open_close_with_time(sym,strat_params["h_time"][i])
        
        dat=pd.DataFrame(dat)

        fin_price.append(0.5*dat.loc[dat.index[-1], 'open']+0.5*dat.loc[dat.index[-1], 'close'])
        dat=dat.iloc[:-1]
        strat_params["cost"].append(0.5*dat.loc[dat.index[-1], 'open']+0.5*dat.loc[dat.index[-1], 'close'])
        tot_data.append(get_reuturn_data(dat))
        if(use_opt):
           stats.append(pred_return(get_distri(dat),yf_opt.options_chain(sym)))
        else:
           stats.append(pred_return(get_distri(dat))) 
    
    if(use_opt):
      cov=np.zeros((strat_params["N"],strat_params["N"]))
      for i in range(strat_params["N"]):
         cov[i,i]=stats[i]["variance"]
    else:
      cov=get_cov_matrix(tot_data)
    ret_arr=np.array([[strat_params["cost"][i]*stats[i]["mean"]] for i in range(strat_params["N"])])
    pr_arr=np.array([[strat_params["cost"][i]] for i in range(strat_params["N"])])

    objective=cp.Maximize(ret_arr.T@vars)
    

    constraints=[cp.quad_form(vars,cov) <=strat_params["risk"],pr_arr.T@vars<=strat_params["inv_limit"]]
    for i in range(strat_params["N"]):
        constraints.append(vars[i]>=0)

    prob=cp.Problem(objective,constraints)
    prob.solve()

    #check if there is indeed a solution::
    rounded=np.array([custom_rounding(vars[i].value[0],2) for i in range(strat_params["N"])])
    org=np.array([vars[i].value[0] for i in range(strat_params["N"])])
    app=(ret_arr.T@np.array(rounded))/(ret_arr.T@np.array(org))
    
    return rounded,app,np.dot(rounded, np.dot(cov, rounded))-np.dot(org, np.dot(cov,org)),pr_arr.T@rounded-pr_arr.T@org,(pr_arr+ret_arr).T@rounded/(pr_arr.T@rounded),(np.array(fin_price).T@rounded)/(np.array(strat_params["cost"]).T@rounded)


    
def compute_strat_running(strat_params,dat_tot,ind=False,use_opt=False):
    
    vars=cp.Variable((strat_params["N"],1))
    stats=[]
    #construct cost::
    strat_params["cost"]=[]
    #strat_params["cost"]=yf_eq.get_curr_cost(strat_params["symbols"])
    tot_data=[]
    fin_price=[]
    for i in range(strat_params["N"]):
        sym=strat_params["symbols"][i]
        #dat=yf_eq.get_open_close_with_time(sym,strat_params["h_time"][i])
        dat=dat_tot[i]
        fin_price.append(0.5*dat.loc[dat.index[-1], 'open']+0.5*dat.loc[dat.index[-1], 'close'])
        dat=dat.iloc[:-1]
        strat_params["cost"].append(0.5*dat.loc[dat.index[-1], 'open']+0.5*dat.loc[dat.index[-1], 'close'])
        tot_data.append(get_reuturn_data(dat))
        if(use_opt):
           stats.append(pred_return(get_distri(dat),yf_opt.options_chain(sym)))
        else:
           stats.append(pred_return(get_distri(dat))) 
    
    if(use_opt or ind):
      cov=np.zeros((strat_params["N"],strat_params["N"]))
      for i in range(strat_params["N"]):
         cov[i,i]=stats[i]["variance"]
    else:
      cov=get_cov_matrix(tot_data)
    ret_arr=np.array([[strat_params["cost"][i]*stats[i]["mean"]] for i in range(strat_params["N"])])
    pr_arr=np.array([[strat_params["cost"][i]] for i in range(strat_params["N"])])

    objective=cp.Maximize(ret_arr.T@vars)
    

    constraints=[cp.quad_form(vars,cov) <=strat_params["risk"],pr_arr.T@vars<=strat_params["inv_limit"]]
    for i in range(strat_params["N"]):
        constraints.append(vars[i]>=0)

    prob=cp.Problem(objective,constraints)
    prob.solve()

    #check if there is indeed a solution::
    rounded=np.array([custom_rounding(vars[i].value[0],2) for i in range(strat_params["N"])])
    org=np.array([vars[i].value[0] for i in range(strat_params["N"])])
    app=(ret_arr.T@np.array(rounded))/(ret_arr.T@np.array(org))
    return rounded,app,np.dot(rounded, np.dot(cov, rounded))-np.dot(org, np.dot(cov,org)),pr_arr.T@rounded-pr_arr.T@org,(ret_arr+pr_arr).T@rounded/(pr_arr.T@rounded),(np.array(fin_price).T@rounded)/(pr_arr.T@rounded)

def compute_strat_momentum(strat_params,dat_tot):
    vars=cp.Variable((strat_params["N"],1))
    stats=[]
    #construct cost::
    strat_params["cost"]=[]
    #strat_params["cost"]=yf_eq.get_curr_cost(strat_params["symbols"])
    tot_data=[]
    fin_price=[]
    for i in range(strat_params["N"]):
        sym=strat_params["symbols"][i]
        #dat=yf_eq.get_open_close_with_time(sym,strat_params["h_time"][i])
        dat=dat_tot[i]
        fin_price.append(0.5*dat.loc[dat.index[-1], 'open']+0.5*dat.loc[dat.index[-1], 'close'])
        dat=dat.iloc[:-1]
        strat_params["cost"].append(0.5*dat.loc[dat.index[-1], 'open']+0.5*dat.loc[dat.index[-1], 'close'])
        tot_data.append(get_reuturn_data(dat))
        
        stats.append(pred_return(get_distri(dat))) 
    
   
    cov=np.zeros((strat_params["N"],strat_params["N"]))
      
    ret_arr=np.array([[strat_params["cost"][i]*stats[i]["mean"]] for i in range(strat_params["N"])])
    pr_arr=np.array([[strat_params["cost"][i]] for i in range(strat_params["N"])])

    objective=cp.Maximize(ret_arr.T@vars)
    

    constraints=[pr_arr.T@vars<=strat_params["inv_limit"]]
    for i in range(strat_params["N"]):
        constraints.append(vars[i]>=0)

    prob=cp.Problem(objective,constraints)
    prob.solve()

    #check if there is indeed a solution::
    rounded=np.array([custom_rounding(vars[i].value[0],2) for i in range(strat_params["N"])])
    org=np.array([vars[i].value[0] for i in range(strat_params["N"])])
    app=(ret_arr.T@np.array(rounded))/(ret_arr.T@np.array(org))
    return rounded,app,np.dot(rounded, np.dot(cov, rounded))-np.dot(org, np.dot(cov,org)),pr_arr.T@rounded-pr_arr.T@org,(ret_arr+pr_arr).T@rounded/(pr_arr.T@rounded),(np.array(fin_price).T@rounded)/(pr_arr.T@rounded)


def run_strat_v1(cfg_file):
    #reads the cfg file and runs the strat using compute_strat
    
    params=import_module("cfg."+cfg_file).cfg
 
    
    alphas,app_factor=compute_strat(params)

    #execute the strat
    return alphas,app_factor,params

if __name__=="__main__":
    #plot_option_data('DIS')
    run_strat_v1("cfg2")