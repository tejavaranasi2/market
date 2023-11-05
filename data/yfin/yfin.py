try:
    import yfinance as yf
    import numpy as np
except:
    print("Import error: [data]")
    exit()


def get_open_close_with_time(sym,t):
  #t is time in months
  s_data=yf.Ticker(sym)
  hist=s_data.history(period=f"{t}mo")
  op=hist["Open"]
  cl=hist["Close"]

  return {"open":np.array(op),"close":np.array(cl)}


def get_curr_cost(sym_lst):
   to_ret=[]
   for sym in sym_lst:
    stock = yf.Ticker(sym)
  
    price = stock.info['regularMarketOpen']
    to_ret.append(price)
   return to_ret

