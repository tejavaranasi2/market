import sys
sys.path.append("../../data/")
import yfin.yfin as yf_eq
import yfin.yfin_options as yf_opt
import numpy as np
import matplotlib.pyplot as plt 
import datetime

def get_reuturn_data(dat):
    mp=0.5*dat["open"]+0.5*dat["close"]#using mid price
    
    if(mp.size==0):
        print("empty data: [strats]")
        return None

    di=np.divide(mp[range(1,mp.size)],mp[range(0,mp.size-1)])
    di=np.log(di)

    return di-np.mean(di)

def get_distri(dat):
    #returns expected distri charecteristics::

    #GBM::

    mp=0.5*dat["open"]+0.5*dat["close"]#using mid price
    
    if(mp.size==0):
        print("empty data: [strats]")
        return None

    di=np.divide(mp[range(1,mp.size)],mp[range(0,mp.size-1)])
    di=np.log(di)

    return {"mean":np.mean(di),"std":np.std(di)}

def get_cov_matrix(data):
    #gets input as data and returns a cov matrix::
    d_arr=np.array(data)
    
    return np.matmul(d_arr,d_arr.T)

def plot_option_data(sym):
    od=yf_opt.options_chain(sym)
  
    call_data=od[od["CALL"]]
    put_data=od[~od["CALL"]]

    #plot call data::
    plt.title(f"Ivol vs strike {sym}")
    plt.xlabel(f"Strike")
    plt.ylabel(f"Ivol")
    plt.plot(call_data["strike"],call_data["impliedVolatility"],"r^")


    #plot put data::
    plt.plot(put_data["strike"],put_data["impliedVolatility"],"b^")
    plt.legend(["call","put"])
    plt.savefig(f"./plots/{sym}vol-k.png")
    
    plt.close()

    #--> tte vs ivol
     #plot call data::
    plt.title(f"Ivol vs dte {sym}")
    plt.xlabel(f"dte")
    plt.ylabel(f"Ivol")
    plt.plot(call_data["dte"],call_data["impliedVolatility"],"r^")


    #plot put data::
    plt.plot(put_data["dte"],put_data["impliedVolatility"],"b^")
    plt.legend(["call","put"])
    plt.savefig(f"./plots/{sym}vol-dte.png")

    plt.close()


    #-->plot ivol for series of dte's::
    tte_arr=np.unique(od["expirationDate"])
    for t in tte_arr:
        tmp_call=call_data[call_data["expirationDate"]==t]
        tmp_put=put_data[put_data["expirationDate"]==t]
        tte=(int)(np.mean(od[od["expirationDate"]==t]["dte"])*365)
        plt.title(f"Ivol vs strike {sym} {tte}")
        plt.xlabel(f"strike")
        plt.ylabel(f"Ivol")
        plt.plot(tmp_call["strike"],tmp_call["impliedVolatility"],"r^")


        #plot put data::
        plt.plot(tmp_put["strike"],tmp_put["impliedVolatility"],"b^")
        plt.legend(["call","put"])
        plt.savefig(f"./plots/{sym}-{tte}_vol-strike.png")

        plt.close()

def get_option_distri(dat,od):
    #od has option data::
    #we should do polynomial extrapolation(currenlty doing mean )
    pass


def pred_return(dist,od=None):
    #given distribution, we try to output mean and variance of the return
    if(od is None or od.size==0):

        mn=np.exp(dist["mean"]+0.5*dist["std"]**2)
        var=(mn**2)*(np.exp(dist["std"]**2)-1)
        mn=mn-1#percentage return::
        return {"mean":mn,"variance":var}
    else:
        std=np.mean(od["impliedVolatility"])#get better metrics by polynomial interpolation::
        
        mn=np.exp(dist["mean"]+0.5*std**2)
        var=(mn**2)*(np.exp(std**2)-1)
        mn =mn-1#perentage return::
        return {"mean":mn,"variance":var}
    
   
