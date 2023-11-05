import sys
sys.path.append("../../data/")
import yfin.yfin as yf_eq
import yfin.yfin_options as yf_opt
import numpy as np

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


def pred_return(dist):
    #given distribution, we try to output mean and variance of the return
    mn=np.exp(dist["mean"]+0.5*dist["std"]**2)
    var=(mn**2)*(np.exp(dist["std"]**2)-1)
    
    return {"mean":mn,"variance":var}

