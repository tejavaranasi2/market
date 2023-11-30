import sys
sys.path.append("../../data/")
import yfin.yfin as yf_eq
import yfin.yfin_options as yf_opt
import numpy as np
import matplotlib.pyplot as plt 
import datetime
import math 
import random
import pandas as pd 
from functools import partial

def get_reuturn_data(dat):
    mp=0.5*dat["open"]+0.5*dat["close"]#using mid price
    mp=np.array(mp)

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
    mp=np.array(mp)

    if(mp.size==0):
        print("empty data: [strats]")
        return None

    di=np.divide(mp[range(1,mp.size)],mp[range(0,mp.size-1)])
    di=np.log(di)

    return {"mean":np.mean(di),"std":np.std(di)}

def get_cov_matrix(data):
    #gets input as data and returns a cov matrix::
    #print(data)
    try:
      d_arr=np.array(data)
    except:
      print(data)
    
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
    
   
def custom_rounding(p,type):
    x=math.floor(p)
    if(type==0):
       return x
    elif(type==1):
       return x+1
    else:
       def bernoulli(p):
        """Simulate a Bernoulli random variable with success probability p."""
        if 0 <= p <= 1:
            return 1 if random.random() < p else 0
        else:
            raise ValueError("p must be between 0 and 1")


       p1=p-x
       if(bernoulli(p1)==1):
           return x+1
       else:
           return x
           

def plot_3d(x,y,z,fig_name):
    colors = z

    # Create a 3D scatter plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(x, y, z, c=colors, cmap='viridis', s=50)

    # Customize plot appearance
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    ax.set_title('3D Scatter Plot with Color Gradient')

    # Add colorbar
    cbar = fig.colorbar(scatter, ax=ax, pad=0.1)
    cbar.set_label('Z Values')

    # Beautify the plot
    ax.grid(True)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('black')
    ax.yaxis.pane.set_edgecolor('black')
    ax.zaxis.pane.set_edgecolor('black')

    # Show the plot

    plt.savefig(fig_name)
       

def generate_test(n):
    cfg_arr=[]
    df=pd.read_csv("test_data/nasdaq_screener.csv")
    l_sym=list(df[df["0"]].Symbol)
    
    for i in range(n):
        cfg={}
        random_number = random.randint(5, 25)
        cfg['N']=random_number
        
        cfg["symbols"]=random.sample(l_sym,random_number)
        cfg["h_time"]=[2 for i in range(random_number)]
        cfg["inv_limit"]=10e4
        cfg["risk"]=0.4
        cfg_arr.append(cfg)
    return cfg_arr



def plot_arrays(array1, array2, label1, label2):
    """
    Plot two arrays against indices on the same graph.

    Parameters:
    - array1: First array to be plotted.
    - array2: Second array to be plotted.
    - xlabel: Label for the x-axis.
    - ylabel: Label for the y-axis.
    """
   
    indices = range(len(array1))  # Assuming both arrays have the same length

    # Plot the first array
    plt.plot(indices, array1, label=label1)

    # Plot the second array
    plt.plot(indices, array2, label=label2)

    # Set labels and title
    plt.xlabel("time")
    plt.ylabel("valuation")
    plt.title(f"{label1} vs {label2}")

    # Add legend
    plt.legend()

   

    plt.savefig(f"plots/{label1}-{label2}.png")
    plt.close()


