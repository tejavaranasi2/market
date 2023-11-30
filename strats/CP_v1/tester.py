from utils import *
from strat import *
test_set=[]

def test_rounding():
    #tests rounding part of the algorithm by using various instances::
    #print a 3-D graph here and talk about rounding::
    x=[]
    y=[]
    z=[]
    pred_ret=[]
    actual_ret=[]
    n=[]
    test_set=generate_test(100)
    # with open("output.csv","w") as fp:
    #     fp.write(f"x,y,z,pred_ret,actual_ret,n\n")
    for cfg in test_set:
      print(f"handling {cfg['N']} stocks {cfg['symbols']}")
      alpha,app_err,var_err,pr_err,p_r,a_r=compute_strat(cfg)
      
      x.append(pr_err)
      y.append(var_err)
      z.append(app_err)
      pred_ret.append(p_r)
      actual_ret.append(a_r)
      n.append(cfg['N'])

      with open("output1.csv","a") as fp:
        fp.write(f"{pr_err[0]},{var_err},{app_err[0]},{p_r[0]},{a_r},{cfg['N']}\n")
    
   
    plot_3d(x,y,z,"plots/rounding_error.png")
    
    #test wrt to number of instruments::

 
def test_ivol_hvol():
    test_set=generate_test(100)
    # with open("output.csv","w") as fp:
    #     fp.write(f"x,y,z,pred_ret,actual_ret,n\n")
    pr_ivol=[]
    ac_ivol=[]

    pr_hvol=[]
    ac_hvol=[]

    n_arr=[]
    # with open("output_ivol_hvol.csv","w") as fp:
    #     fp.write(f"p1,a1,p2,a2,n\n")
    for cfg in test_set:
      print(f"handling {cfg['N']} stocks {cfg['symbols']}")
      try:
        alpha_1,app_err_1,var_err_1,pr_err_1,p_r_1,a_r_1=compute_strat(cfg)
        alpha_2,app_err_2,var_err_2,pr_err_2,p_r_2,a_r_2=compute_strat(cfg,True)
      except:
        continue
      pr_ivol.append(p_r_1)
      ac_ivol.append(a_r_1)

      pr_hvol.append(p_r_2)
      ac_hvol.append(a_r_2)

      
     
      n_arr.append(cfg['N'])

      with open("output_ivol_hvol1.csv","a") as fp:
        fp.write(f"{p_r_1},{a_r_1},{p_r_2},{a_r_2},{cfg['N']}\n")
def performance_test(strat1,strat2,s1_name,s2_name):
    #efficacy of momentum traing::

    #fix a cfg and run a 12 yr interval by preparing data::
    cfg=generate_test(1)[0]

    
    dat=[]
    T=10**10

    for i in range(cfg['N']):
        dat.append(pd.DataFrame(yf_eq.get_open_close_with_time(cfg['symbols'][i],12)))
        T=min(dat[i]["close"].size,T)#number of days::
    print(f"handling {cfg['N']} stocks for {T} days")
    net_val_strat1=[1]
    net_val_strat2=[1]

    net_pred_val_strat1=[1]
    net_pred_val_strat2=[1]
   
    
    for i in range(60,T):
       dat_temp=[]
       for j in range(cfg['N']):
        dat_temp.append(dat[j].iloc[i-60:i])
       alpha_1,app_err_1,var_err_1,pr_err_1,p_r_1,a_r_1=strat1(cfg,dat_temp)
       alpha_2,app_err_2,var_err_2,pr_err_2,p_r_2,a_r_2=strat2(cfg,dat_temp)
       
       net_val_strat1.append(net_val_strat1[-1]*a_r_1[0])
       net_val_strat2.append(net_val_strat2[-1]*a_r_2[0])

       net_pred_val_strat1.append(net_val_strat1[-1]*p_r_1[0])
       net_pred_val_strat2.append(net_val_strat2[-1]*p_r_2[0])
       
       
    plot_arrays(net_val_strat1,net_pred_val_strat1,s1_name,"expected")
    plot_arrays(net_val_strat2,net_pred_val_strat2,s2_name,"expected")
    plot_arrays(net_val_strat1,net_val_strat2,s1_name,s2_name)

   






#performance_test(compute_strat_running,compute_strat_momentum,"CP","momentum")
performance_test(compute_strat_running,partial(compute_strat_running,ind=True),"CP","CP_ind")
#test_ivol_hvol()